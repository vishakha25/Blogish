Assignment 1:


'''
form1="""
<form method="post" >
    What is your Birthday?
    <br>
    <label>Month
    <input type="text" name="month" value="%(month)s">
    </label>
    
    <label>Day
    <input type="text" name="day" value="%(day)s">
    </label>
    
    <label>Year
    <input type="text" name="year" value="%(year)s">
    </label>
    
    <div style="color:red">%(error)s</div>
    
    <br>
    <br>  
 <input type="submit"> 
</form> """

class DateHandler(webapp2.RequestHandler):
    
    #setting default values for write_form
    def write_form(self,error="",month="",day="",year=""):
     # checking for special characters        
        def escape_html(s):
            for(i,o) in (("&", "&amp;"),
                         (">", "&gt;"),
                         ("<", "&lt;"),
                         ('"', "&quot;")):
                s=s.replace(i,o)
            return s
        self.response.out.write(form % {"error":error,
                                        "month":escape_html(month),
                                        "day":escape_html(day),
                                        "year":escape_html(year)})
    def get(self):
        #self.response.write('<h1>Welcome to Blogish!!!</h1>')
        self.write_form() 
        
    def post(self):
        
        #####################
        # date validation methods
        months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
        month_abbrv=dict((m[:3].lower(),m) for m in months)
       
        def valid_month(month):    
            if month:
                short_month=month[:3].lower()
                #return month_abbrv.get(short_month)
                return True
        def valid_day(day):
            if day and day.isdigit():
                d=int(day)
                if d>0 and d<32:
                    return True
        def valid_year(year):
            if year and year.isdigit():
                y=int(year)
                if y>1900 and y<2020:
                    return True
    
                
        ###########################
        
    
        user_month= self.request.get('month')
        user_day= self.request.get('day')
        user_year= self.request.get('year')
        
        month= valid_month(user_month)
        day=valid_day(user_day)
        year=valid_year(user_year)
        
        
        if not(month and day and year):
            self.write_form("This is invalid, please enter again",user_month,user_day,user_year)
        else:
            self.redirect("/thanks")    
           

    


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Validation Passed")


class TestHandler(webapp2.RequestHandler):
    def post(self):
        #q=self.request.get("q")
        #self.response.write(q)  
        self.response.headers['Content-Type']='text/plain'
        self.response.out.write(self.request)
'''       
         
Assignment 2:


import webapp2
import string
form="""
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;" >%(words)s</textarea>
      <br>
      <input type="submit">
    </form>
"""
class MainHandler(webapp2.RequestHandler):
    def write_form(self,words=""):
        self.response.out.write(form % {"words":words})  
    def get(self):
        self.write_form()
    def post(self):
        ###method to ROT13 the user input
        def convertROT13(word):
           return word.encode('rot13')
    
        user_text=self.request.get('text')
        rot13Text=convertROT13(user_text)
        self.write_form(rot13Text)
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
   # ('/thanks',ThanksHandler),
    #('/testform',TestHandler)
], debug=True)

         
         
         
         
         