import os, urllib
#import jinja2
import webapp2

## JINJA_ENVIRONMENT = jinja2.Environment(
##     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
##     extensions=['jinja2.ext.autoescape'],
##     autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
    
    def post(self):
        mbid  =  request.POST.get('mbid')
        track_name =  request.POST.get('track_name')            
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(mbid + ' ' + track_name)

        
        
        ## template = JINJA_ENVIRONMENT.get_template('index.html')
        ## self.response.write(template)

## def record_user_location(request):
##     print "JS request.COOKIES", request.COOKIES
##     user_id = request.COOKIES.get('u')
##     if not user_id:
##         user_id = str( uuid.uuid4() )
##     print "user_id", user_id
##     user, created = CookieUser.objects.get_or_create(user_id=user_id)

##     user.save()
##     print user

##     return HttpResponse('')

application = webapp2.WSGIApplication([
    ('/py/', MainPage),
], debug=True)
