import yaml
import json




#функция сравнивает леммы
def compareLemmas(rule_elem, data_elem):
	lexes = rule_elem['Lex'].split('|')
	print(lexes)
	for lex in lexes:
		lex = lex.replace(' ', '')
		print(lex)
		if lex in data_elem['lemma']:
			return True
		else:
			return False


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
					print('morph tag from the rule not found', tag)
					return False
			elif 'NOT' in tag:
				tag = tag.split(':')[1]
				if tag not in data_elem['tagsets'][0]:
					continue
				else:
					print('wrong tag found')
					return False
			else:
				if tag not in data_elem['tagsets'][0]:
					print('morph tag from the rule not found', tag)
					return False
	#сравниваем леммы
	if rule_elem['Lex']:
		if compareLemmas(rule_elem, data_elem):
			return True
		else:
			return False
	return True


#функция находит и равнивает вершины из данных и из правила
def compareHeads(rule, data):
	for elem in data[0]['tokens']:
		if elem['parent_token_index'] == -1: #нашли вершину в предложении
			head = elem
	for elem in rule['Items']:
		if 'ConstituentType' in elem and 'Lex' in elem:
			rule_head = elem
		else:
			"не нашли вершину в правиле"
	#сравниваем constit type
	rule_const_types = rule_head['ConstituentType'].split('|')
	for const_type in rule_const_types:
		const_type = const_type.replace(' ', '')
		if head['constituent']['name'] == const_type:
			#сравниваем морф теги
			if compareMorphTags(rule_head, head):
				print('Морф теги совпали')
			else:
				print('Морф теги не совпали')
		elif (head['constituent']['name'] != const_type) and (rule_const_types[-1] == const_type):
			print("типы состовл не совпали в вершинах, переходим к след правилу")
	
	head_letter = list(rule_head.keys())[0]
	return head, rule_head, head_letter 

#функция сравнивает леммы из правил (Lex) с леммами из данных
def checkLexes(rule, data):
	lemmas = []
	lexes = []
	flag = True
	for elem in data[0]['tokens']:
		lemmas.append(elem["lemma"])
	for elem in rule['Items']:
		if 'Lex' in elem:
			lex = elem['Lex'].replace(' ', '')
			lexes.append(lex)
	for lex in lexes:
		if lex not in lemmas:
			if '|' in lex:
				cur_lexes = lex.split('|')
				for cur_lex in cur_lexes:
					if cur_lex in lemmas:
						idx = lemmas.index(cur_lex)
						lemmas.pop(idx)
						break
					if cur_lex not in lemmas and cur_lex == cur_lexes[-1]:
						flag = False
			else:
				print('lex from rule absents')
				flag = False
				break
		else:
			idx = lemmas.index(lex)
			lemmas.pop(idx)
	return flag



with open("Rules/PainIncreases1.yaml", 'r') as f:
    rule = yaml.safe_load(f)

with open("output2.json", "r") as f2:
    data = json.load(f2)


for elem in rule['Items']:
	if 'Lex' in elem:
		if not checkLexes(rule, data): #переходим к следующему правилу. пока условие будет следующим
			print("lexes не совпали в правиле и в json файле")
		else:
			compareHeads(rule, data)
			break
