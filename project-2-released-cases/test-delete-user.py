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

	#create griffin
	PARAMS = {'first_name': 'Griffin', 'last_name': 'Klev', 'username': 'griffin', 'email_address': 'k@griffin.com', 'password': 'Igapfakbsm2', 'salt': 'K8ENdhu#nxe3'}
	r = requests.post(url = URL, data = PARAMS)

	#create and fieri
	PARAMS = {'first_name': 'Guy', 'last_name': 'Fieri', 'username': 'fieri', 'email_address': 'guy@fieri.com', 'password': 'Igapfakbsm2', 'salt': 'Sbw3vgd#asv'}
	r = requests.post(url = URL, data = PARAMS)


	#create recipe by jmm
	URLCreateRecipe = "http://127.0.0.1:5000/create_recipe"
	RECIPEPARAMS = {'name': 'Scrambled Eggs', 'description': 'These eggs will knock your socks off. Step 1: Cook the eggs', 'recipe_id': 524, 'ingredients': json.dumps(['eggs', 'love'])}
	r_create_recipe = requests.post(url = URLCreateRecipe, data = RECIPEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f'})

	#like recipe by griffin
	URLLikeRecipe = "http://127.0.0.1:5000/like"
	LIKEPARAMS = {'recipe_id': 524}
	r_like_recipe = requests.post(url = URLLikeRecipe, data = LIKEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})
	like_recipe_data = r_like_recipe.json()

	#like recipe by fieri
	URLLikeRecipe = "http://127.0.0.1:5000/like"
	LIKEPARAMS = {'recipe_id': 524}
	r_like_recipe = requests.post(url = URLLikeRecipe, data = LIKEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJmaWVyaSJ9.2388b903ac10c4217a82cbed5e8d4a0b985646aa6ceda028245acdd50ee0d558'})
	like_recipe_data = r_like_recipe.json()


	#view recipe by griffin
	URLViewRecipe = "http://127.0.0.1:5000/view_recipe/524"
	VEIWPARAMS = {'name': 'True', 'likes': 'True', 'ingredients': 'True'}
	r_view_recipe = requests.get(url = URLViewRecipe, params = VEIWPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})
	view_data = r_view_recipe.json()

	solution = json.dumps({'status': 1, 'data': {'name': 'Scrambled Eggs', 'ingredients': ['love', 'eggs'], 'likes': '2'}})
	solution_dict = json.loads(solution)

	
	if len(view_data['data']) != len(solution_dict['data']):
		quit()

	for x in solution_dict['data']:
		if x == 'ingredients':
			if len(solution_dict['data'][x]) != len(view_data['data'][x]):
				quit()
			else:
				for ingredient in view_data['data'][x]:
					if ingredient not in solution_dict['data'][x]:
						quit()
							
		elif solution_dict['data'][x] != view_data['data'][x]:
			quit()

	#delete account by fieri
	URLDelete = "http://127.0.0.1:5000/delete"
	DELETEPARAMS = {'username': 'fieri'}
	r_delete = requests.post(url = URLDelete, data = DELETEPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJmaWVyaSJ9.2388b903ac10c4217a82cbed5e8d4a0b985646aa6ceda028245acdd50ee0d558'})

	#view recipe by griffin
	URLViewRecipe = "http://127.0.0.1:5000/view_recipe/524"
	VEIWPARAMS = {'name': 'True', 'likes': 'True', 'ingredients': 'True'}
	r_view_recipe = requests.get(url = URLViewRecipe, params = VEIWPARAMS, headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJncmlmZmluIn0=.803e985bbf6d4da2b9f42d0de4f33539396ecf4d82b2bffde2d29adf7d36aedb'})
	view_data = r_view_recipe.json()

	solution = json.dumps({'status': 1, 'data': {'name': 'Scrambled Eggs', 'ingredients': ['love', 'eggs'], 'likes': '1'}})
	solution_dict = json.loads(solution)

	
	if len(view_data['data']) != len(solution_dict['data']):
		quit()

	for x in solution_dict['data']:
		if x == 'ingredients':
			if len(solution_dict['data'][x]) != len(view_data['data'][x]):
				quit()
			else:
				for ingredient in view_data['data'][x]:
					if ingredient not in solution_dict['data'][x]:
						quit()
							
		elif solution_dict['data'][x] != view_data['data'][x]:
			quit()

	print('Test Passed')

except:
	print('Test Failed')

