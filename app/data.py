import pandas as pd
drugs = []

drugs.append({"name":"Keytruda","company":"Merck","link":"https://www.keytrudahcp.com"})
drugs.append({"name":"Opdivo","company":"Bristol Myers Squibb","link":"https://www.opdivohcp.com"})
drugs.append({"name":"Kisqali","company":"Novartis","link":"https://www.kisqali-hcp.com"})
drugs.append({"name":"Imfinzi","company":"AstraZeneca","link":"https://www.imfinzihcp.com"})
drugs.append({"name":"Tecentriq","company":"Genentech","link":"https://www.tecentriq-hcp.com"})
drugs.append({"name":"Enhertu","company":"Daiichi-Sankyo AstraZeneca","link":"https://www.enhertuhcp.com/en/mbc"})

doctors_data = []
doctors_data.append({"Name":"Sarah Wilson","Speciality":"Dermatology","City":"New York","State":"CA","Last Visit":"2020-04-27","email_ok":False,"visits_ok":False,"tries_new_drugs":True,"needs_data":False,"email_address":"sarah.wilson@doctor.net"})
doctors_data.append({"Name":"John Miller","Speciality":"Gastroenterology","City":"Dallas","State":"AZ","Last Visit":"2022-03-13","email_ok":False,"visits_ok":True,"tries_new_drugs":True,"needs_data":False,"email_address":"john.miller@medicmail.com"})
doctors_data.append({"Name":"Jane Smith","Speciality":"Urology","City":"Houston","State":"NY","Last Visit":"2023-06-30","email_ok":True,"visits_ok":True,"tries_new_drugs":True,"needs_data":True,"email_address":"jane.smith@example.com"})
doctors_data.append({"Name":"Michael Miller","Speciality":"Dermatology","City":"San Antonio","State":"TX","Last Visit":"2022-04-19","email_ok":True,"visits_ok":True,"tries_new_drugs":True,"needs_data":False,"email_address":"michael.miller@healthcare.org"})
doctors_data.append({"Name":"Katie Brown","Speciality":"Pediatrics","City":"Chicago","State":"AZ","Last Visit":"2019-11-10","email_ok":True,"visits_ok":True,"tries_new_drugs":False,"needs_data":False,"email_address":"katie.brown@healthcare.org"})
doctors_data.append({"Name":"Michael Brown","Speciality":"Psychiatry","City":"San Jose","State":"PA","Last Visit":"2021-09-17","email_ok":False,"visits_ok":True,"tries_new_drugs":False,"needs_data":True,"email_address":"michael.brown@doctor.net"})
doctors_data.append({"Name":"Alex Smith","Speciality":"Cardiology","City":"Philadelphia","State":"TX","Last Visit":"2020-06-04","email_ok":False,"visits_ok":True,"tries_new_drugs":True,"needs_data":False,"email_address":"alex.smith@medicmail.com"})
doctors_data.append({"Name":"David Jones","Speciality":"Cardiology","City":"Phoenix","State":"TX","Last Visit":"2021-10-04","email_ok":True,"visits_ok":False,"tries_new_drugs":False,"needs_data":False,"email_address":"david.jones@healthcare.org"})
doctors_data.append({"Name":"Emily Miller","Speciality":"Psychiatry","City":"Houston","State":"AZ","Last Visit":"2019-10-28","email_ok":True,"visits_ok":True,"tries_new_drugs":False,"needs_data":False,"email_address":"emily.miller@doctor.net"})
doctors_data.append({"Name":"John Smith","Speciality":"Dermatology","City":"Houston","State":"TX","Last Visit":"2020-08-09","email_ok":True,"visits_ok":False,"tries_new_drugs":True,"needs_data":False,"email_address":"john.smith@healthcare.org"})
doctors_data.append({"Name":"John Miller","Speciality":"Gastroenterology","City":"Dallas","State":"IL","Last Visit":"2023-01-09","email_ok":True,"visits_ok":False,"tries_new_drugs":True,"needs_data":True,"email_address":"john.miller@doctor.net"})
doctors_data.append({"Name":"Jane Moore","Speciality":"Cardiology","City":"San Jose","State":"NY","Last Visit":"2022-01-08","email_ok":True,"visits_ok":False,"tries_new_drugs":False,"needs_data":True,"email_address":"jane.moore@example.com"})
doctors_data.append({"Name":"Katie Davis","Speciality":"Urology","City":"San Diego","State":"CA","Last Visit":"2023-10-24","email_ok":True,"visits_ok":False,"tries_new_drugs":True,"needs_data":True,"email_address":"katie.davis@healthcare.org"})
doctors_data.append({"Name":"David Wilson","Speciality":"Dermatology","City":"San Antonio","State":"NY","Last Visit":"2023-04-03","email_ok":False,"visits_ok":True,"tries_new_drugs":False,"needs_data":False,"email_address":"david.wilson@healthcare.org"})
doctors_data.append({"Name":"Laura Taylor","Speciality":"Endocrinology","City":"San Antonio","State":"IL","Last Visit":"2022-06-19","email_ok":False,"visits_ok":False,"tries_new_drugs":True,"needs_data":False,"email_address":"laura.taylor@doctor.net"})
doctors_data.append({"Name":"Emily Williams","Speciality":"Radiology","City":"New York","State":"NY","Last Visit":"2023-02-18","email_ok":True,"visits_ok":True,"tries_new_drugs":True,"needs_data":True,"email_address":"emily.williams@healthcare.org"})
doctors_data.append({"Name":"Alex Jones","Speciality":"Neurology","City":"Los Angeles","State":"PA","Last Visit":"2023-07-23","email_ok":True,"visits_ok":False,"tries_new_drugs":False,"needs_data":True,"email_address":"alex.jones@example.com"})
doctors_data.append({"Name":"John Jones","Speciality":"Dermatology","City":"Chicago","State":"PA","Last Visit":"2020-01-02","email_ok":False,"visits_ok":True,"tries_new_drugs":True,"needs_data":True,"email_address":"john.jones@healthcare.org"})
doctors_data.append({"Name":"David Wilson","Speciality":"Cardiology","City":"San Jose","State":"TX","Last Visit":"2024-07-18","email_ok":True,"visits_ok":False,"tries_new_drugs":False,"needs_data":True,"email_address":"david.wilson@example.com"})
doctors_data.append({"Name":"Alex Smith","Speciality":"Gastroenterology","City":"San Jose","State":"TX","Last Visit":"2024-01-04","email_ok":False,"visits_ok":True,"tries_new_drugs":True,"needs_data":True,"email_address":"alex.smith@doctor.net"})

doctors_df = pd.DataFrame(doctors_data)