#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import string
import re
form="""
    <h1>Signup </h1>
    <form method="post">
    <label>Name
    <input type="text" name="username" value="%(username)s">
    </label>
    <div style="color:red">%(nameerror)s</div>
    
    <label>Password
    <input type="password" name="pass1" value="%(pass1)s">
    </label>
     <div style="color:red">%(passerror)s</div>
    
    <label>Verify Password
    <input type="password" name="pass2" value="%(pass2)s">
    </label>
    <div style="color:red">%(passverifyerror)s</div>
    
    <label>Email(optional)
    <input type="email" name="emailaddress" value="%(emailaddress)s">
    </label>
    <br>
     <input type="submit"> 
</form>

"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self,username="",nameerror="",pass1="",passerror="",pass2="",passverifyerror="",emailaddress="",):
        self.response.out.write(form % {"username":username,
                                      "pass1":pass1,
                                      "pass2":pass2,
                                      "emailaddress":emailaddress,
                                      "nameerror":nameerror,
                                      "passerror":passerror,
                                      "passverifyerror":passverifyerror})  
    def get(self):
        self.write_form()
    def post(self):
        user_username= self.request.get('username')
        user_pass1=self.request.get('pass1')
        user_pass2=self.request.get('pass2')
        user_emailaddress=self.request.get('emailaddress')
        def valid_username(username):
            USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
            if not (USER_RE.match(username)):
                return "That's not a valid username."
            else:
                return ""
        def valid_password(pw1,pw2):
            PASS_RE= re.compile(r"^.{3,20}$")
            if not(PASS_RE.match(pw1) or PASS_RE.match(pw2)):
                return "That wasn't a valid password."
            else:
                return ""
        def valid_passwordMatch(pw1,pw2):
            if not(pw1==pw2):
                return "Your passwords didn't match"  
            else:
                return "" 
        
        nameerror=valid_username(user_username)
        passerror=valid_password(user_pass1,user_pass2)
        passverifyerror=valid_passwordMatch(user_pass1, user_pass2)
        
        if(nameerror or passerror or passverifyerror):
            self.write_form(user_username, nameerror, user_pass1, passerror, user_pass2, passverifyerror, user_emailaddress)
        else:    
            self.redirect("/welcome?username=" + user_username)
            
class WelcomeHandler(webapp2.RequestHandler): 
    def get(self):
        name=self.request.get('username')
        self.response.out.write("Welcome, %s!" % name )
 
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',WelcomeHandler)
], debug=True)

