####################################
# Improving upon tag replacement
# script using regular expresions

import re
template_dir = "./template_backups/"
project_dir = "../microblog/app/templates/"

files_with_tags = [
    
    "login.html",
    "500.html",
    "404.html",    
    "reset_password.html",
    "base.html",
    "reset_password_request.html",
    "email/reset_password.html",
    "edit_profile.html",
    "_post.html",
    "user.html",
    "index.html",
    "register.html",

]


tags = {

    "atag"  : re.compile('>[\w!?\s]+</a>'),
    "ptag"  : re.compile('<p>[\w!?\s]+<'),
    "h1tag" : re.compile('<h1>[\w!?\s]+</h1>'),
    "alltxt" : re.compile('>[\s]*[\w]+[\w\s!.?]*<')
    
}

def wrapPlainText(textdata, tagp):
    """
    Find next plain text inside html tags as in <sometag>Hello!</sometag>
    that would need to be translated, and wrap with the _() translation 
    function like so, <sometag>_('Hello!')</sometag>
    """
    print(fn,":")

    # Get re iterator
    tag_iterator = tagp.finditer(textdata)

    # Initialize offset
    offset = 0
    
    for match in tag_iterator:
        leftpos, rightpos = (index + offset for index in match.span())
        

        leftxt, tagtxt, rightxt = ( textdata[:leftpos],
                                    textdata[leftpos:rightpos],
                                    textdata[rightpos:] )
        # Replace
        print(tagtxt)        
        tagtxt = ">{{_('" + tagtxt[1:]  # replace left enpoint
        tagtxt = tagtxt[:-1] + "')}}<"  # replace right enpoint
        print(tagtxt)

        offset += len(">{{_('") + len("')}}<") - len(">") - len("<")
        
        # Reconstruct text in file
        textdata = leftxt + tagtxt + rightxt


        print("-----------\n")
    
    return textdata

    
################################
# Loop through all template files
for fn in files_with_tags:
    
    with open(template_dir + fn + ".bak", "r") as f:
        file_data = f.read()

    # Debug
    # print("\n-------\n", fn, ":")
    # wrapPlaintext(file_data, tags["alltxt"])
    # print("------------")

    file_data = wrapPlainText(file_data, tags["alltxt"])

    with open(template_dir + fn, "w") as result:
    # with open(project_dir + fn, "w") as result:
        result.write(file_data)  
