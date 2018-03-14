import requests, json, re


if __name__ == "__main__":

	transcripts = json.load(open('data/transcripts_db_dump.json'))
	transcripts_counts = json.load(open('data/transcripts_counts.json'))


	authority = json.load(open('data/authority_cleaned.json'))

	missing_interviewers = []
	for t in transcripts:

		# find the interviewee in the authority, make sure it is there, add the slug
		for a in authority:
			if t['intervieweeURI'] == a['uri']:
				t['ljSlug'] = a['ljSlug']


		t['interviewers'] = re.sub('\s+',' ',t['interviewers'])
		t['interviewers'] = t['interviewers'].replace(', ',',')
		t['interviewers'] = list(set(t['interviewers'].split(',')))
		t['interviewers_ljSlug'] = []

		for i in t['interviewers']:

			slug = i.replace(' ','_')
			for a in authority:
				if slug == a['ljSlug']:
					t['interviewers_ljSlug'].append(slug)

			if slug not in t['interviewers_ljSlug']:
				if i != '':
					missing_interviewers.append(i)
					

		# we are going to do this again, creating the missing ones 
		t['interviewers_ljSlug'] = []

		for c in transcripts_counts:
			if c['transcript'] == t['md5']:
				t['totalPairs'] = c['totalPairs']
				t['totalResponse'] = c['totalResponse']


	# build data for interviewers
	built_interviewers = []
	for i in list(set(missing_interviewers)):

		slug = i.replace(' ','_')
		built_interviewers.append({"name":i, "ljSlug":slug, "type":"interviewer"})

	orgs = []

	for t in transcripts:
		for i in t['interviewers']:
			if i == '':
				continue

			slug = i.replace(' ','_')
			for a in authority:
				if slug == a['ljSlug']:
					t['interviewers_ljSlug'].append(slug)

			for a in built_interviewers:
				if slug == a['ljSlug']:
					t['interviewers_ljSlug'].append(slug)


			# make sure
			assert slug in t['interviewers_ljSlug']


		if t['sourceName'] not in orgs:
			orgs.append(t['sourceName'])




	built_orgs = []
	for o in orgs:
		built_orgs.append({"name":o.replace('_',' '),"ljSlug":o})


	
	json.dump(transcripts,open('data/transcripts_documents.json','w'),indent=2)
	json.dump(built_interviewers,open('data/transcripts_interviewers.json','w'),indent=2)
	json.dump(built_orgs,open('data/transcripts_orgs.json','w'),indent=2)
