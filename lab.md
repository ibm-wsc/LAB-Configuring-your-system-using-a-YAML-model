# Configuring your system using a YAML model
This session is intended to get you comfortable with the tooling and processes necessary to configure z/OS with a YAML model. It is necessarily simplified and merely a model to show how things will work and to help you get comfortable with the processes. It is not using a real system’s YAML, rather one focused only on the configuration of a z/OS Unix environment. It assumes you have a python3 environment on your machine.
## Pre-Lab Checklist
 - Python 3.13+ installed
 - VSCode installed (optional)
 - YAML & Jinja extensions added
 - Files downloaded:
    - UnixInfo.yaml
    - zOSUnixParms.schema.json
    - BPXPRM.jinja,
    - parmlibbuild.py
## Setup
If you do not have a python environment on your machine, you can get one by downloading it from: https://www.python.org/downloads/release/python-3135/

In addition to Python, you will need to install two packages:
- pyYAML to read YAML files
- Jinja2 to build the parmlib member from YAML

These packages can be installed on your system using the pip command.

- Type `pip3 install PyYAML` to install the YAML reader
- Type `pip3 install JINJA2` to install jinja on your platform

In addition to these you will need 4 things from us:
- UnixInfo.yaml – The YAML file that includes the definitions for a Unix environment on Z.
- zOSUnixParms.schema.json – The rules governing z/OS Unix configuration
- BPXPRM.jinja – The Jinja template that is used to map out the changes
- parmlibbuild.py – The code to build a parmlib member using YAML as the source and a map to the parmlib member.

You can use any IDE that you wish to edit the data. If you need one, you can download VSCode from: https://code.visualstudio.com/download

### VSCode Setup
If you have VSCode, you probably want to add the YAML extension from Red Hat.
It would be good to get the Jinja extension too.
You will have to update the VSCode YAML extension to point to the Schema we have shared with you.
Once installed go to the extension settings and in the YAML section you will see something that says to edit settings.json:

Figure 1: Configuring the editor
Click on this and add in the yaml.schema section:
"yaml.schemas": {
"/path/zOSUnixParms.schema.json":"*.zosunixinfo.yaml"
},
Where path is the location of the schema file you downloaded.
Once all of this is done you are ready to configure your system’s Unix.
## The Steps
There are three different components in this lab:
- The YAML edit. In this section you will edit a z/OS Unix configuration. In it you can get a feel for the way things are setup and how you will add content and change existing content.
- The JINJA Template Edit. In real life you will never have to deal with the tooling that converts the YAML into PARMLIB. This section will give you the opportunity to see how we map the YAML into the PARMLIB dataset
- Run the conversion. Rather than running than running the conversion on a z/OS system, we will build a file on your machine that will be the content that lives in a parmlib member.

### Component 1: Edit the YAML file
Find the YAML file in your file browser and edit it with VSCode. You should see something like this:
![VSCode](path/to/image.jpg "Figure 2: The YAML in a VSCode editor")

What you are looking at is the configuration information displayed in a whole new way. Rather than using the 8 character codes for different configuration elements, you are seeing descriptive definitions. The data is defined in Key Value pairs. They keys are separated from the values by a `:`.

In some cases the values associated with the key is a list of values. The list is identified by the – character. Each line is another element in the list. This allows you to have multiple values for the same key. You can see that step_library_list points to multiple files.
Sometimes the list value may itself be a complex object contain its own set of key value pairs. This is evidenced in the file_system_type_info: entries. They define a file system type and other data about that entry (like the entry point)

It is pretty obvious that the system recognizes the difference between characters and numbers allowing us to perform some basic checking on each entry. 

Let’s begin by adding an entry to the configuration.

1. Put you mouse over the entry auto_convert. 
    - What happens? You should see a box pop up. It not only tells you what auto_convert does, it provides the allowed values.
1. Bring your cursor to the end of maximum_number_of_threads line (after the number) and press enter. 
1. Then type: max
    - You should see several possible entries that can be added to the configuration. It will only show you entries you are allowed to add. If you look closely you will notice that none of the entries that are currently in the file are listed in the drop down list.
1. Click on maximum_number_of_shared_pages. 
    - This will bring the entry into the editor along with its default value of 131072. Let’s assume you don’t want to use the default value.
1. Type in 999999999 (that’s nine nines).
    - What do you notice about the number you just entered. Also check out the filename at the top. It should have turned red. Also a red squiggly line has appeared under the number. 
1. If you bring your mouse over the red squiggly lines what happens?
    - Since according to the error message 999999999 is too large 
1. Let’s try a smaller number. Type: -1
    - You will notice that the red squiggly line has returned. What is the error now? 
1. Let’s just return it to the default of 131072
    - How is this black magic accomplished? When you setup VSCode to support YAML files we added to the configuration a JSON SCHEMA. This schema is the rules for how to handle the yaml file.

![VSCode](path/to/image.jpg "Figure 3: VSCode supporting editing the YAML file")

When you updated the configuration file you told VSCode that whenever it saw a file that ended with zosunixinfo.yaml, that it should use the json schema file zOSUnixParms.schema.json for the rules on how the data should be managed. The cool thing is that these same rules will work in other Integrated Development Environment. There are even standalone editors like vim, that will support these rules.

Further down the file you will find the entries for file systems that are automatically mounted in the z/OS Unix environment. Scroll through them until you find one that supports having Java mounted on the system. Where is it mounted? What kind of file system is it?
Now that we have made changes in the file let’s save it. You can click on Save at the top of the screen and close the edit session.
When you are doing this for real, the configuration would be saved in git or some other source code-controlled environment. There would be a review process with content from you about what you changed and why that would be part of the review process for the change. We will skip that part for now.

### Component 2: Build the Parmlib member
Now that we have a valid YAML file let’s use it to build the parmlib member that you would see in sys1.parmlib. Instead of building the member on z/OS we will create it as a file on your workstation.

1. Type: `parmlibbuild.py -y UnixInfo.yaml -t bpxprm.jinja -m bpxprmxx`
    - (Where xx are your initials).  
    - Once it is complete we can look at the output.

1. Look at the file using your favorite editor. 
    - Of course you can open it with VSCode as your editor but don’t expect any special coloring or checking since there is no support for PARMLIB text in a file.

At the top of the file you should see a banner. Notice that the banner shows the name of the file you edited as the source. It also presents a date and time stamp when the file was created. It also warns you not to edit the file directly since it was created with automation.

This is exactly what you would see if you built it into parmlib.
How does this work? The parmlibbuild.py is a program that takes the YAML input, turns it into a structure. It then uses a jinja template to figure out how to create the member. You will never have to touch this template. IBM will provide it along with the JSON schema. As a user you will be responsible for the YAML file only. The rest will be up to IBM.

![VSCode](path/to/image.jpg "Figure 4: Building a parmlib member from YAML")

Jinja is a standard templating technology that many use to create dynamic web pages. Using a set of rules, it allows us to create a parmlib member based on data in the YAML file and the contents of the template.
Even though you will never have to touch one of these templates, let’s look at it to show how this technology works.

### Component 3: Changing the template
Let’s go back into VSCode and edit our jinja template.

1. Find the file BPXPRM.jinja in your file browser and edit it with VSCode. You should see something like this:

![VSCode](path/to/image.jpg "Figure 5:BPXPRM Jinja template")

If what you see isn’t color coded it is because your VSCode does not recognize the jinja file type. You could add a VSCode extension for it but it is hardly worth it since you won’t be touching this file in the future.

At the top of the file you should see the eyecatcher that was in the output file you built. You will notice a set of lines that are merely content the is meant to be rendered. The first two lines are just text in the file.

On the third line you will see a variable called now. We know it is a variable because it sits between a pair of curly braces. The `{{now}}` tells jinja that instead of typing this content out get the value of now and put it there. Similarly, Jinja will replace the `{{source_file}}` with the name of the source file that we pass into the program. We The program automatically creates these variables and provides them when the template calls for it.

When we edited the YAML file you will recall that there are possible entries that we didn’t add to the system. The template must be sensitive to this so each entry is located prior to printing.

Lines 7-11 represent everything needed to handle a normal entry on the system. We start with a check to see if the variable we want has been defined. All jinja commands start with {% and end with %} So we begin by asking jinja if a variable exists. If component_trace_member is defined, then we will perform all of the following lines until we get to an {% endif%}.
Line 8 tells jinja to write everything in upper case. This is in case the user put the content in lower case. The {% filter upper %} will put everything in upper case until it finds a {% endfilter %} statement.

Finally on line 9 we have the CTRACE setting with the variable in the parenthesis.
Any changes we put in the template will be reflected in the output. 

1. Let’s input a new line after line2. Make the line: # Template modified by {{%name}}

![VSCode](path/to/image.jpg "Figure 6:Update Template")

1. Save this template. Now go back into your YAML file and add an entry at the top. The entry should be:
    - Name: ‘Your Name’
        - Where Your Name is your name. 
1. Save this. Now we can try the buildparm.py program again. 
    - Did the new parmlib member contain your name?

Now look through the jinja template and see other control structures. Can you figure out the for loop that takes the content from the YAML file and put it into the format that you see in your created member?
# Conclusion
This sample gives you an idea of how the configuration will be managed in a YAML environment. The real version will be completer and more complex. This simple session is intended to give you the idea of how the entire system will work.

Updated configurations will be delivered along with system updates, ensuring that the rules for entering data in the YAML file and the template for creating parmlib from the yaml file will continuously be up to date.

