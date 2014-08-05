import os, json, datetime
import requests
import webapp2
from operator import itemgetter

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
        year_count_dict = {}
        track_string = "u'%s'" % track_name.lower()
        for setlist in setlist_array:
            sets = repr(setlist.get('sets')).lower()
            if track_string in sets:
                total_playcount += 1
                event_date = setlist.get('@eventDate')
                event_year =  event_date[event_date.rfind('-')+1:]
                year_count_dict[event_year] = year_count_dict.get(event_year, 0) + 1
        year_count_array = sorted(year_count_dict.items(), key=itemgetter(0), reverse=True)                
                
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write( json.dumps({'total_playcount': total_playcount, 'year_count_array': year_count_array}) )

application = webapp2.WSGIApplication([
    ('/py/setlist/', SetlistInfo),
], debug=True)
