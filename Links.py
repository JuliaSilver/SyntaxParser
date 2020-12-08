import yaml
import json


def checkLinks(rule, data):
	print(rule['Links'])

#функция возвращает true, если все морфологические теги совпали
def compareMorphTags(rule_elem, data_elem):
	#print(rule_elem)
	if 'Morph' in rule_elem:
		rule_morph_tags = rule_elem['Morph'].split(',')
		for elem in rule_morph_tags:
			tag = elem.replace(' ', '')
			if '|' in tag:
				tag1, tag2 = tag.split('|')
				if tag1 in data_elem['tagsets'][0] or tag2 in data_elem['tagsets'][0]:
					continue
				else:
					print('морф тег из правила не найден', tag)
					return False
			elif 'NOT' in tag:
				tag = tag.split(':')[1]
				if tag not in data_elem['tagsets'][0]:
					continue
				else:
					print('неправильный морф тег найден в json')
					return False
			else:
				if tag not in data_elem['tagsets'][0]:
					print('морф тег из правила не найден', tag)
					return False
	return True

#функция сравнивает леммы
def compareTags(rule_elem, data_elem, participant, matched_pairs):
	flag = False #в качестве метки для найденой леммы из правили 
	#print(matched_pairs, 'matched_pairs')
	#print(list(matched_pairs.values()), 'list(matched_pairs.values())')
	print(rule_elem)
	if 'Lex' in rule_elem:
		lexes = rule_elem['Lex'].split('|')
		lexes = [lex.replace(' ', '') for lex in lexes]
		for elem in data_elem['tokens']:
			if elem['itoken'] not in list(matched_pairs.values()):
				#print(elem['lemma'])
				if elem['lemma'] in lexes:
					if (elem['constituent']['is_head'] == True) and ('Lex' in rule_elem):
						flag = True
						if compareConstitTypes(rule_elem, elem):
							matched_pairs[participant] = elem['itoken']
							print("лемма и тип сост совпали", elem, rule_elem)
							if compareMorphTags(rule_elem, elem):
								print("морф теги совпали", elem, rule_elem)
								#if checkLinks()
								break
							else:
								print("морф теги не совпали", elem, rule_elem)

			if (elem == data_elem['tokens'][-1]) and not flag:
				print('лемма из правила не найдена или is_head не совпало с тегом Lex/LexNonHead')
	elif 'LexNonHead' in rule_elem:
		print('LexNonHead')
		lexes = rule_elem['LexNonHead'].split('|')
		lexes = [lex.replace(' ', '') for lex in lexes]
		for elem in data_elem['tokens']:
			if elem['itoken'] not in list(matched_pairs.values()):
				print(elem['lemma'])
				if elem['lemma'] in lexes:
					if (elem['constituent']['is_head'] == False) and ('LexNonHead' in rule_elem):
						flag = True
						if compareConstitTypes(rule_elem, elem):
							matched_pairs[participant] = elem['itoken']
							print("лемма и тип сост совпали", elem, rule_elem)
							if compareMorphTags(rule_elem, elem):
								print("морф теги совпали")
								break
							else:
								print("морф теги не совпали")
			if (elem == data_elem['tokens'][-1]) and not flag:
				print('лемма из правила не найдена или is_head не совпало с тегом Lex/LexNonHead')

	else:
		for elem in data_elem['tokens']:
			if elem['itoken'] not in list(matched_pairs.values()):
				if compareConstitTypes(rule_elem, elem):
					matched_pairs[participant] = elem['itoken']
					print("леммы нет тип сост совпал", elem, rule_elem)
					if compareMorphTags(rule_elem, elem):
						print("морф теги совпали", elem, rule_elem)
						break
					else:
						print("морф теги не совпали")

	return False

def compareConstitTypes(rule_elem, data_elem):
	if 'ConstituentType' in rule_elem:
		rule_const_types = rule_elem['ConstituentType'].split('|')
		for const_type in rule_const_types:
			const_type = const_type.replace(' ', '')
		if data_elem['constituent']['name'] == const_type:
			return True
		else:
			return False
	else:
		return True



def ifLinkExists(tokens, sec_itoken, first_itoken):
	for token in tokens:
		if token['itoken'] == sec_itoken:
			print(sec_itoken, 'sec_itoken в функ')
			print(first_itoken, 'first_itoken в функ')
			#print(token['parent_token_index'], token, 'у этого токена в родителях стоит секонд')
			print('djjdjd', token['parent_token_index'])
			if token['parent_token_index'] == first_itoken:
				return True
			else:
				#for token2 in tokens:
					#if token2['itoken'] == token['parent_token_index']:
				ifLinkExists(data[0]['tokens'], token['parent_token_index'], first_itoken)






with open("Rules/PainIncreases1.yaml", 'r') as f:
    rule = yaml.safe_load(f)

with open("output.json", "r") as f2:
    data = json.load(f2)

participants = rule['Participants']
matched_pairs = {'A': [0], 'B': [3, 2], 'C': [1], 'D': [4]}
#for elem in matched_pairs:
#links = rule['Links']
links = {'D,A': 'any'}
#firs_letter, sec_letter = letters.split(',')
#cur_link = links[letters]
for key in links:
	print(key, 'key')
	cur_link = links[key]
	letters = key.split(',')
	first_applicants = matched_pairs[letters[0]]
	sec_applicants = matched_pairs[letters[1]]
	for sec_itoken in sec_applicants:
		print(sec_itoken, 'sec_itoken')
		for first_itoken in first_applicants:
			print(first_itoken, 'first_itoken')
			for token in data[0]['tokens']:
				if token['itoken'] == sec_itoken: #нашла А
					#print(token['edge_type'])
					if (token['edge_type'] == cur_link) and (token['parent_token_index'] == first_itoken):
						print('тип связи совпал')
						break
					elif (cur_link == 'one') or (cur_link == 'any'):
						if token['parent_token_index'] == first_itoken: #смотрим на родителя А
							print('тип связи one или any совпал', token['parent_token_index'])
							break
						else:
							# если родитель А не Д
							print('родитель у А не Д') # берем родителя а и смотрим его родителя
							if ifLinkExists(data[0]['tokens'], token['parent_token_index'], first_itoken):
								print('1')
							#cur_parent_token_index = token['parent_token_index']
							#for elem in token['itoken']:
								#if elem == cur_parent_token_index: #нашли родительский токен
									#if cur_parent_token_index == sec_itoken:
										#flag = True
										#print('тип связи any совпал')







