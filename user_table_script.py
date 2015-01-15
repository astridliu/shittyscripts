from bs4 import BeautifulSoup
import sys, json, re, os
import glob

# Data for User related table


f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_table_new.txt', 'w')
f.write('user_id' + '\t' + 'user_name' + '\t' + 'user_profile_id' + '\t' + 'user_about_me_intro' + '\t' + 'user_about_me_status' + '\t' + 'user_about_me_best_answer' + '\t' + 'user_about_me_top_answer' + '\t' + 'user_about_me_rate' + '\t' + 'user_about_me_interest_tag_name' + '\t' + 'user_about_me_more\n')
f.close()
print "user_table_new.txt prepared"

f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_community_table_new.txt', 'w')
f.write('forum_id' + 'user_id\n')
f.close()
print "user_community_table_new.txt prepared"

f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_journal_table_new.txt', 'w')
f.write('journal_id' + '\t' + 'journal_title' + '\t' + 'journal_time' + '\t' + 'journal_content' + '\t' + 'journal_reply' + '\t' + 'user_id\n')
f.close()
print "user_journal_table_new.txt prepared"

f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_note_table_new.txt', 'w')
f.write('note_id' + '\t' + 'user_id_sender' + '\t' + 'note_time' + '\t' + 'note_content' + '\t' + 'user_id_receiver\n')
f.close()
print "user_note_table_new.txt prepared"

f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_status_table_new.txt', 'w')
f.write('status_id' + '\t' + 'status_time' + '\t' + 'status_content' + '\t' + 'status_reply' + '\t' + 'user_id\n')
f.close()
print "user_status_table_new.txt prepared"

f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_tracker_table_new.txt', 'w')
f.write('tracker_id' + '\t' + 'tracker_name' + '\t' + 'user_id\n')
f.close()
print "user_tracker_table_new.txt"


# f = open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/tag_table_u1.txt', 'w')
# f.write('tag_url' + '\t' + 'tag_name\n')
# f.close()


count = 1
error = 1

id_regex = re.compile(r'[0-9]+')
comment_id_regex = re.compile(r'post_[0-9]+')


path = r'/storage4/foreseer/users/liulu/report/tasks0928/new_user/html'
for filename in glob.iglob(os.path.join(path, '*.html')):
	# try:
		# t = re.match(r"1([0-9]+)\.html", str(filename.split('/')[-1])).group()

	with open(filename) as file:
		html_doc = file.read()
		soup = BeautifulSoup(html_doc)
		file.close()


# user_table

	if soup.find('div', { 'class' : 'leave_note'}):
		user_id = soup.find('div', { 'class' : 'leave_note'}).a['data-user'].encode('utf8').strip()
	else:
		user_id = os.path.splitext(filename)[0].strip(path)
		
	if soup.find('div', { 'class' : 'page_title'}):
		user_name = soup.find('div', { 'class' : 'page_title'}).get_text().encode('utf8').strip().split('\'')[0]
		user_profile_id = soup.find('span', { 'class' : 'pp_r_txt_sel'}).a.get('href').encode('utf8').strip().split('=')[-1]

		temp_about_me = soup.find('div', { 'class' : 'section'}).get_text().strip().encode('utf8').replace('\xa0', ' ').replace('\xc2', ' ')
		if temp_about_me:
			user_about_me_intro = temp_about_me.split(':')[1].replace('\t', ' ').strip()
			user_about_me_intro = os.linesep.join([s for s in user_about_me_intro.splitlines() if s.strip()])
			user_about_me_intro = "".join(line.strip() for line in user_about_me_intro.split("\n"))
			user_about_me_intro = "".join(line.strip() for line in user_about_me_intro.split("\t"))
		else:
			user_about_me_intro = 'None'
	
		temp = soup.find('div', { 'id' : 'mood'})
		if temp:
			user_about_me_status = soup.find('div', { 'id' : 'mood'}).get_text().strip().encode('utf8').replace('\xa0', ' ').replace('\xc2', ' ')
		else:
			user_about_me_status = 'None'

		temp_bestanswer = soup.find('div', { 'id' : 'best_answers_hover'})
		if temp_bestanswer.get_text().encode().strip():
			user_about_me_best_answer = int(id_regex.search(temp_bestanswer.get_text().encode('utf8').strip()).group())
		else:
			user_about_me_best_answer = 0
		
		temp_topanswer = soup.find('div', { 'class' : 'stars extra_info float_fix'})
		user_about_me_top_answer = ''
		if temp_topanswer:
			for item in temp_topanswer.find_all('div', {'class' : 'subcategory_name'}):
				if user_about_me_top_answer:
					user_about_me_top_answer = user_about_me_top_answer + ', ' + item.get_text().encode('utf8').strip()
				else:
					user_about_me_top_answer = item.get_text().encode('utf8').strip()

			num_list = []
			for item in temp_topanswer.find_all('div'):
				# print item.get("class")[0].encode()
				if item.get('class')[0].encode() != "subcategory_name" and item.get('class')[0].encode() != "title":
					# print item.get('class')[0].encode().split('_')[1]
					num_list.append(item.get('class')[0].encode().split('_')[1])
			num_str = ",".join(num_list)



		else:
			user_about_me_top_answer = 'None'
			num_str = 'None'


	
		temp_interest = soup.find('span', { 'class' : 'interests'})
		if temp_interest:
			user_about_me_interest_tag_name = temp_interest.find('span', { 'class' : 'interests_show'}).get_text().encode('utf8').strip()
			if temp_interest.find('span', { 'class' : 'interests_less'}):
				user_about_me_interest_tag_name = user_about_me_interest_tag_name + temp_interest.find('span', { 'class' : 'interests_less'}).get_text().encode('utf8').strip().replace('[Less]', '')				
		else:
			user_about_me_interest_tag_name = 'None'					
					
		temp_about_more = soup.find('span', { 'class' : 'about_me_show'})
		if temp_about_more:
			temp_about_more = soup.find('span', { 'class' : 'about_me_show'}).get_text().encode('utf8').strip().replace('\xa0', ' ').replace('\xc2', ' ')
			temp_about_less = soup.find('span', { 'id' : 'about_me_less'})
			if temp_about_less:
				temp_about_less = soup.find('span', { 'id' : 'about_me_less'}).get_text(' ','<br/>').encode('utf8').strip().replace('\xa0', ' ').replace('\xc2', ' ')
				user_about_me_more = (temp_about_more + temp_about_less).strip('[Less]').strip()
			else:
				user_about_me_more = temp_about_more
			# lines = []
			# lines = user_about_me_more.split()
			# for line in lines:
			# 	line = line.strip()
			# 	user_about_me_more.join(line)
			user_about_me_more = user_about_me_more.replace('\t', ' ').strip()
			user_about_me_more = os.linesep.join([s for s in user_about_me_more.splitlines() if s.strip()])
			user_about_me_more = "".join(line.strip() for line in user_about_me_more.split("\n"))
			user_about_me_more = "".join(line.strip() for line in user_about_me_more.split("\t"))		
		else:
			user_about_me_more = 'None'
		
		with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_table_new.txt', 'a') as f:
			f.write(user_id + '\t' + user_name + '\t' + user_profile_id + '\t'+ user_about_me_intro + '\t' + user_about_me_status + '\t' + str(user_about_me_best_answer) + '\t' + user_about_me_top_answer + '\t' + str(num_str) + '\t' + user_about_me_interest_tag_name + '\t'+ user_about_me_more + '\n')
		print file.name.split('/')[-1] + ' file ' + str(user_id) + ' user table completed!'

# user_community_table

	
	if soup.find('div', { 'class' : 'page_title'}):
		temp = soup.find('div', { 'id' : 'my_comm'})
		if temp:
			if temp.find_all('div', { 'class' : 'comm_name'}): # optional
				for item in temp.find_all('div', { 'class' : 'comm_name'}):
					if item.find('img', { 'class' : 'c_disc_icon_xs icon_img_ww'}):
						link = str(item.find('img', { 'class' : 'c_disc_icon_xs icon_img_ww'}).a.get('href'))
						temp_id = id_regex.search(link).group(0).encode('utf8').strip()
						with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_community_table_new.txt', 'a') as f:
							f.write(temp_id + '\t' + user_id + '\n')
						print file.name.split('/')[-1] + ' file ' + str(user_id) + ' user community table completed!'



					elif item.find('img', { 'class' : 'ug_comm_list_icon icon_img_ww'}):
						link = str(item.find('img', { 'class' : 'ug_comm_list_icon icon_img_ww'}).a.get('href'))
						temp_id = id_regex.search(link).group(0).encode('utf8').strip()
						with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_community_table_new.txt', 'a') as f:
							f.write(temp_id + '\t' + user_id + '\n')
						print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user community table completed!'
							
							
# user_journal_table



	if soup.find('div', { 'class' : 'page_title'}):
		temp = soup.find('div', { 'class' : 'list float_fix'})
		if temp.find_all('div', { 'class' : 'journal_entry'}):
			for item in temp.find_all('div', { 'class' : 'journal_entry'}):
				temp_title = item.find('div', { 'class' : 'user_journal_summary_title'}).get_text().encode('utf8').strip()
				temp_postid = item['id'].encode().strip().split('_')[-1]
				temp_time = item.find_all('span', {'class' : 'date'})[0].get_text().encode('utf8').strip()
				temp_reply = id_regex.search(item.find_all('span', {'class' : 'date'})[1].get_text().encode('utf8').strip()).group()
				temp_content = item.find('div', {'class' : 'content'}).get_text().encode('utf8').strip(item.find('div', {'class' : 'head'}).get_text().encode('utf8')).strip('\n').strip('\r').strip().replace('\n', '').replace('\r', '').replace('\xa0', ' ').replace('\xc2', ' ')
				temp_content = temp_content.replace('\t', ' ').strip()
				temp_content = os.linesep.join([s for s in temp_content.splitlines() if s.strip()])
				temp_content = "".join(line.strip() for line in temp_content.split("\n"))
				temp_content = "".join(line.strip() for line in temp_content.split("\t"))
				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_journal_table_new.txt', 'a') as f:
					f.write(temp_postid + '\t' + temp_title + '\t' + temp_time + '\t' + temp_content + '\t' + str(temp_reply) + '\t' + user_id + '\n')
				print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user journal table completed!'
				
	
# user_note_table


	if soup.find('div', { 'class' : 'page_title'}):
		temp_note = soup.find('div', { 'id' : 'up_notes_list'})
		if temp_note.find('div', { 'class' : 'note_entries'}):
			for item in temp_note.find_all('div', { 'class' : 'note_entry float_fix'}):
				note_id = item['id'].encode('utf8').strip()
				user_id_sender = id_regex.search(str(item.find('span').a.get('href').encode('utf8').strip())).group()
				note_time = item.find('div', { 'class' : 'note_desc'}).find_all('div')[1].get_text().encode('utf8').strip()
				note_content = item.find('div', { 'class' : 'note_msg'}).get_text('\n','<br/>').encode('utf8').strip().replace('\n', '').replace('\t', '')
				note_content = os.linesep.join([s for s in note_content.splitlines() if s.strip()])
				note_content = "".join(line.strip() for line in note_content.split("\n"))
				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_note_table_new.txt', 'a') as f:
					f.write(note_id + '\t' + user_id_sender + '\t' + note_time + '\t' + note_content + '\t' + user_id + '\n')
				print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user note table completed!'
				
				
				
			for item in temp_note.find_all('div', { 'class' : 'note_entry float_fix note_sep'}):
				note_id = item['id'].encode('utf8').strip()
				user_id_sender = id_regex.search(str(item.find('span').a.get('href').encode('utf8').strip())).group()
				note_time = item.find('div', { 'class' : 'note_desc'}).find_all('div')[1].get_text().encode('utf8').strip()
				note_content = item.find('div', { 'class' : 'note_msg'}).get_text('\n','<br/>').encode('utf8').strip().replace('\n', '').replace('\t', '')
				note_content = os.linesep.join([s for s in note_content.splitlines() if s.strip()])
				note_content = "".join(line.strip() for line in note_content.split("\n"))
				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_note_table_new.txt', 'a') as f:
					f.write(note_id + '\t' + user_id_sender + '\t' + note_time + '\t' + note_content + '\t' + user_id + '\n')
				print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user note table completed!'
				

# user_status_table



	if soup.find('div', { 'class' : 'page_title'}):
		temp = soup.find('div', { 'class' : 'status_list float_fix'})
		if temp.find_all('div', { 'class' : 'status float_fix '}):
			for item in temp.find_all('div', { 'class' : 'status float_fix '}):
				temp_id = item['data-status-id'].encode('utf8').strip()
				temp_time = item.find('span', {'class' : 'time'}).get_text().encode('utf8').replace('\xa0', ' ').replace('\xc2', ' ').replace('-', ' ').strip()
				temp_content = item.find('span', {'class' : 'text'}).get_text().encode('utf8').replace('\xa0', ' ').replace('\xc2', ' ').replace('-', ' ').strip()
				temp_reply = item.find('span', {'class' : 'comment_count'}).get_text().encode('utf8').replace('\xa0', ' ').replace('\xc2', ' ').replace('-', ' ').strip()
				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_status_table_new.txt', 'a') as f:
					f.write(temp_id + '\t' + temp_time + '\t' + temp_content + '\t' + str(temp_reply) + '\t' + user_id + '\n')
				print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user status table completed!'
				
				
# user_tracker_table

		
	if soup.find('div', { 'class' : 'page_title'}):
		temp = soup.find('div', { 'id' : 'wg_content_8'})
		if temp.find_all('div', { 'class' : 'ut_side_item float_fix'}):
			for item in temp.find_all('div', { 'class' : 'ut_side_item float_fix'}):
				temp_name = item.find('div', { 'class' : 'ut_side_link'}).get_text().encode('utf8').strip()
				link = item.find('div', { 'class' : 'ut_side_link'}).a.get('href')
				temp_id = id_regex.search(link).group(0).encode('utf8').strip()
				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_tracker_table_new.txt', 'a') as f:
					f.write(temp_id + '\t' + temp_name + '\t' + user_id + '\n')
				print file.name.split('/')[-1] + ' file ' +  str(user_id) + ' user tracker table completed!'


# tag


	# temp_interest = soup.find('span', { 'class' : 'interests'})
	# if temp_interest:
	# 	temp_interest1 = temp_interest.find('span', { 'class' : 'interests_show'})
	# 	for item in temp_interest1.find_all('a'):
	# 		tag_name = item.get_text().encode().strip()
	# 		tag_id = item.get('href').encode('utf8').strip()
	# 		with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/tag_table_u1.txt', 'a') as f:
	# 			f.write(tag_id + '\t' + tag_name + '\n')		
	# 		print tag_name + ' tag recorded!'
			
			
						
	# 	temp_interest2 = temp_interest.find('span', { 'id' : 'interests_less'})
	# 	if temp_interest2:
	# 		for item in temp_interest2.find_all('a'):
	# 			tag_name = item.get_text().encode().strip()
	# 			tag_id = item.get('href').encode('utf8').strip()
	# 			if tag_name != '[Less]':
	# 				with open('/storage4/foreseer/users/liulu/report/tasks0928/new_user/tag_table_u1.txt', 'a') as f:
	# 					f.write(tag_id + '\t' + tag_name + '\n')		
	# 				print tag_name + ' tag recorded!'
					
					

	with open("/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_log_new.txt", 'a') as f_log:
		f_log.write(file.name.split('/')[-1] + '\t' + str(count) + '\n')
		
	count += 1
	
	print file.name.split('/')[-1] + ' file completed!'

# except:
# 	# with open("jump.txt", "a") as record:
# 		# record.write(os.path.splitext(filename)[0].strip(path) + '\n')

# 	print 'Skip Error or non-qualified file !!' + '\t' + str(error)
# 	with open("/storage4/foreseer/users/liulu/report/tasks0928/new_user/user_log_error.txt", 'a') as f_log:
# 		f_log.write(file.name.split('/')[-1] + '\t' + str(error) + '\n')
# 	error += 1

# 	continue						