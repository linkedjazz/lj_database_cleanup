import requests, json
import tqdm
import multiprocessing







# for idx, p in enumerate(authority):

def download_dbpedia(p):

	if p['uri'].find('dbpedia') > -1:

		data_uri = p['uri'].replace('<','').replace('>','').replace('/resource/','/data/') + '.json'

		r = requests.get(data_uri)
		if r.status_code == 200:

			dbpedia_slug = p['uri'].replace('<','').replace('>','').split('http://dbpedia.org/resource/')[1]
			p['dbpediaSlug'] = dbpedia_slug

			data = r.json()
			for l1 in data:

				for l2 in data[l1]:

					if l2 == 'http://www.w3.org/2002/07/owl#sameAs':
						for sameAs in data[l1][l2]:
							if sameAs['value'].find('wikidata.org/entity/') > -1:
								qid = sameAs['value'].split('http://www.wikidata.org/entity/')[1]
								p['wikidata'] = qid								

		else:

			p['bad_dbpedia_uri'] = True

	else:

		p['no_dbpedia_uri'] = True

	return p


if __name__ == "__main__":


	authority = json.load(open('data/authority.json'))
	results = []

	counter = 0
	lock = multiprocessing.Lock()

	for result in tqdm.tqdm(multiprocessing.Pool(10).imap_unordered(download_dbpedia, authority), total=len(authority)):	
		counter+= 1
		# print(result)
		results.append(result)

		if counter % 10 == 0:
			lock.acquire()
			json.dump(results,open('data/authority_with_wikidata_ids.json','w'),indent=2)
			lock.release()


	json.dump(results,open('data/authority_with_wikidata_ids.json','w'),indent=2)
