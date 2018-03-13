import requests, json


if __name__ == "__main__":

	authority = json.load(open('data/authority_with_wikidata_ids.json'))


	for p in authority:

		if p['uri'].find('id.loc.gov') > -1:

			lccn = p['uri'].replace('<','').replace('>','').replace('.html','').split('/names/')[1]
			

			viaf_url = "http://viaf.org/viaf/lccn/"+lccn+"/justlinks.json"


			r = requests.get(viaf_url)
			if r.status_code == 200:
				data = r.json()
				if 'WKP' in data:
					p['wikidata'] = data['WKP'][0]
				
	





	json.dump(authority,open('data/authority_with_wikidata_ids_from_viaf.json','w'),indent=2)
