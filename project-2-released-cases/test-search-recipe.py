import requests
import json

try:
	URLclear = "http://127.0.0.1:5000/clear"
	r_clear = requests.get(url = URLclear)
	 
	#create and login jmm
	URL = "http://127.0.0.1:5000/create_user"
	PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'jmm', 'email_address': 'james@mariani.com', 'password': 'Examplepassword1', 'salt': 'FE8x1gO+7z0B'}

	r = requests.post(url = URL, data = PARAMS)

	URLLogin = "http://127.0.0.1:5000/login"
	LOGINPARAMS = {'username': 'jmm', 'password': 'Examplepassword1'}
	r_login = requests.post(url = URLLogin, data = LOGINPARAMS)

	#create and login griffin
	PARAMS = {'first_name': 'Griffin', 'last_name': 'Klev', 'username': 'griffin', 'email_address': 'k@griffin.com', 'password': 'Igapfakbsm2', 'salt': 'K8ENdhu#nxe3'}
	r = requests.post(url = URL, data = PARAMS)

	LOGINPARAMS = {'username': 'griffin', 'password': 'Igapfakbsm2'}
	r_login = requests.post(url = URLLogin, data = LOGINPARAMS)

	#create recipe by jmm
	URLCreateRecipe = "http://127.0.0.1:5000/create_recipe"
	RECIPEPARAMS = {'name': 'Scrambled Eggs', 'description': 'These eggs will knock your socks off. Step 1: Cook the eggs', 'recipe_id': 524, 'ingredients': json.dumps(['eggs', 'love'])}
	r_create_recipe = requests.post(url = URLCreateRecipe, data = RECIPEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f'})

	#create recipe by jmm
	URLCreateRecipe = "http://127.0.0.1:5000/create_recipe"
	RECIPEPARAMS = {'name': 'Toast Sandwich', 'description': 'Why can I not enjoy my food??', 'recipe_id': 127, 'ingredients': json.dumps(['bread'])}
	r_create_recipe = requests.post(url = URLCreateRecipe, data = RECIPEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f'})

	#create recipe by jmm
	URLCreateRecipe = "http://127.0.0.1:5000/create_recipe"
	RECIPEPARAMS = {'name': 'Oatmeal Raisin Cookies', 'description': 'Oh, these are not chocolate chip?', 'recipe_id': 601, 'ingredients': json.dumps(['flour', 'oatmeal', 'butter', 'raisins'])}
	r_create_recipe = requests.post(url = URLCreateRecipe, data = RECIPEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f'})

	#like recipe by griffin
	URLLikeRecipe = "http://127.0.0.1:5000/like"
	LIKEPARAMS = {'recipe_id': 601}
	r_like_recipe = requests.post(url = URLLikeRecipe, data = LIKEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})
	like_recipe_data = r_like_recipe.json()

	#follow jmm by griffin
	URLFollow = "http://127.0.0.1:5000/follow"
	FOLLOWPARAMS = {'username': 'jmm'}
	r_follow = requests.post(url = URLFollow, data = FOLLOWPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})


	#search by feed by griffin
	URLSearchFeed = "http://127.0.0.1:5000/search"
	SEARCHPARAMS = {'feed': 'True'}
	r_search = requests.get(url = URLSearchFeed, params = SEARCHPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})
	search_data = r_search.json()

	solution = json.dumps({'status': 1, 'data': {601: {'name': 'Oatmeal Raisin Cookies', 'description': 'Oh, these are not chocolate chip?', 'ingredients': ['flour', 'oatmeal', 'butter', 'raisins'], 'likes': '1'}, 127: {'name': 'Toast Sandwich', 'description': 'Why can I not enjoy my food??', 'ingredients': ['bread'], 'likes': '0'}}})
	solution_dict = json.loads(solution)

	if len(search_data['data']) != len(solution_dict['data']):
		quit()

	for recipe in solution_dict['data']:
		if len(solution_dict['data'][recipe]) != len(search_data['data'][recipe]):
			quit()
		for x in solution_dict['data'][recipe]:
			if x == 'ingredients':
				if len(solution_dict['data'][recipe][x]) != len(search_data['data'][recipe][x]):
					quit()
				else:
					for ingredient in search_data['data'][recipe][x]:
						if ingredient not in solution_dict['data'][recipe][x]:
							quit()

								
			elif solution_dict['data'][recipe][x] != search_data['data'][recipe][x]:
				quit()

	print('Test Passed')
except:
	print('Test Failed')

