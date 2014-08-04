import os, json
import requests
import webapp2

## JINJA_ENVIRONMENT = jinja2.Environment(
##     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
##     extensions=['jinja2.ext.autoescape'],
##     autoescape=True)

class SetlistInfo(webapp2.RequestHandler):

    def post(self):
        request_json = json.loads(self.request.body)
        mbid  =  request_json.get('mbid')
        track_name =  request_json.get('track_name')
        api_artist_url = 'http://api.setlist.fm/rest/0.1/artist/%s.json' % mbid
        api_artist_request = requests.get(api_artist_url)
        api_json = json.loads(api_artist_request.text)
        artist = api_json.get('artist')
        artist_url = artist.get('url')
        artist_slug = artist_url[artist_url.rfind('/')+1:]
        track_url = 'http://www.setlist.fm/stats/songs/%s?song=%s' % (artist_slug, track_name)
        track_html = requests.get(track_url).text
        print track_html
        self.response.headers['Content-Type'] = 'text/plain'        
#        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(artist_url)
        
        ## template = JINJA_ENVIRONMENT.get_template('index.html')
        ## self.response.write(template)

## def record_user_location(request):
##     print "JS request.COOKIES", request.COOKIES
##     user_id = request.COOKIES.get('u')
##     if not user_id:
##         user_id = str( uuid.uuid4() )
##     print "user_id", user_id
##     user, created = CookieUser.objects.get_or_create(user_id=user_id)
##     user.last_known_latitude =  request.POST.get('latitude')
##     user.last_known_longitude =  request.POST.get('longitude')    
##     user.save()
##     print user

##     return HttpResponse('')

application = webapp2.WSGIApplication([
    ('/py/setlist/', SetlistInfo),
], debug=True)
