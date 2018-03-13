import requests, json


if __name__ == "__main__":

	authority = json.load(open('data/authority_with_wikidata_ids_from_viaf.json'))
	slugs = []

	for p in authority:


		if p['uri'] == '<http://dbpedia.org/resource/Charles_Davis_(saxophonist)>':
			p['name'] = 'Charles_Davis_(saxophonist)'

		if p['uri'] == '<http://dbpedia.org/resource/George_Butler_(record_producer)>':
			p['name'] = 'George_Butler_(record_producer)'


		slug = p['name'].replace(' ','_')

		if slug not in slugs:
			p['ljSlug'] = slug
			slugs.append(slug)
		else:
			print('dupe',p)


		if p['uri'].find('id.loc.gov') > -1:
			lccn = p['uri'].replace('<','').replace('>','').replace('.html','').split('/names/')[1]
			p['lccn'] = lccn

		if p['uri'].find('linkedjazz.org/resource') > -1:
			p['ljMint'] = True


		if p['uri'].find('musicbrainz.org') > -1:
			musicbrainz = p['uri'].replace('<','').replace('>','').replace('/relationships','').replace('/recordings','').split('/artist/')[1]
			p['musicbrainz'] = musicbrainz

		

		if p['uri'].find('allmusic.com') > -1:
			allmusic = p['uri'].replace('<','').replace('>','').replace('/credits','').replace('/recordings','').split('/artist/')[1]
			p['allmusic'] = allmusic
			



	json.dump(authority,open('data/authority_cleaned.json','w'),indent=2)
