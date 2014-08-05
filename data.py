import os, json, datetime
import requests
import webapp2

artist_setlists_template = 'http://api.setlist.fm/rest/0.1/artist/%s/setlists.json?p=%d'

class SetlistInfo(webapp2.RequestHandler):

    def post(self):
        request_json = json.loads(self.request.body)
        mbid  =  request_json.get('mbid')
        track_name =  request_json.get('track_name')
        initial_api_request = requests.get( artist_setlists_template % (mbid, 1) )
        initial_api_json = json.loads(initial_api_request.text)
        initial_setlists = initial_api_json.get('setlists')
        items_per_page = float(initial_setlists.get('@itemsPerPage'))
        total_items =  float(initial_setlists.get('@total'))
        total_pages_float = total_items / items_per_page
        total_pages = int(total_pages_float)
        if total_pages_float > total_pages:
            total_pages += 1
        setlist_array = initial_setlists.get('setlist')
        for i in range(2, total_pages+1):
            api_request = requests.get( artist_setlists_template % (mbid, i) )
            api_json = json.loads(api_request.text)
            setlists = api_json.get('setlists')
            setlist_array = setlist_array + setlists.get('setlist')

        total_playcount = 0
        play_years = []
        year_count_dict = {}
        track_string = "u'%s'" % track_name.lower()
        for i, setlist in enumerate(setlist_array):
            sets = repr(setlist.get('sets')).lower()
            if track_string in sets:
                total_playcount += 1
                event_date = setlist.get('@eventDate')
                event_year =  event_date[event_date.rfind('-')+1:]
                event_year_int =  int(event_year_string)
                if not event_year_int in play_years:
                    
                    print event_date, "-", i, "-", total_playcount, "-", track_string, " in ", sets
                
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write( json.dumps({}) )
        
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
