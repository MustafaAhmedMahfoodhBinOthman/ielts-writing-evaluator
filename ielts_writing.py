import streamlit as st
st.set_page_config(
    
    page_title= 'IELTS Writing Evaluator'
    # page_icon=
)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
import anthropic
import google.generativeai as genai
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib.pyplot as plt
import random
import re
import os
import csv
import time
import streamlit.components.v1 as components
from dotenv import load_dotenv
# with open("BayanPlusTracking.html", "r") as f:
#     html_code = f.read()
#     components.html(html_code, height=0)



    
st.markdown(
    """
    <style>
        .st-emotion-cache-j7qwjs {
            display: none;
        }
        .st-emotion-cache-sntl9t {
            display: none;
        }
        .st-emotion-cache-1oe5cao {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        transition: margin-left .3s;
    }
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-left: 20rem;
        transition: padding-left .3s;
    }
    .sidebar-expanded .sidebar .sidebar-content {
        margin-left: 0;
    }
    .sidebar-expanded .reportview-container .main .block-container {
        padding-left: 7rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Claude_API_KEY = st.secrets['Claude_API_KEY']
# Gemini_API_Key = st.secrets['Gemini_API_Key'] #mustafabinothman22
# Gemini_API_Key2 = st.secrets['Gemini_API_Key2'] #mustafanotion
# Gemini_API_Key3 = st.secrets['Gemini_API_Key3'] #mustafabinothman2003
# Gemini_API_Key4 = st.secrets['Gemini_API_Key4'] #mustafabinothman2023
# Gemini_API_Key5 = st.secrets['Gemini_API_Key5'] #www.binothman24
Claude_API_KEY = os.getenv('Claude_API_KEY')
Gemini_API_Key = os.getenv('Gemini_API_Key') #mustafabinothman22
Gemini_API_Key2 = os.getenv('Gemini_API_Key2') #mustafanotion
Gemini_API_Key3 = os.getenv('Gemini_API_Key3') #mustafabinothman2003
Gemini_API_Key4 = os.getenv('Gemini_API_Key4') #mustafabinothman2023
Gemini_API_Key5 = os.getenv('Gemini_API_Key5') #www.binothman24

keys = [Gemini_API_Key,Gemini_API_Key2,Gemini_API_Key3,Gemini_API_Key4,Gemini_API_Key5]
used_key = random.choice(keys)


model = genai.GenerativeModel('gemini-1.0-pro-latest')
model_vision = genai.GenerativeModel('gemini-pro-vision')

type_check = 'primary'
type_take = 'secondary'

st.sidebar.title("""
                 
                 
                 
              
                 
                 """)

st.sidebar.title('IELTS Writing Evaluator (Free)')
st.sidebar.write('This is currently in Beta version, and everyday it will be updated to reach better evalaution GOOD LUCK 😊⚡')
# st.sidebar.write('There will be many special features and big improvments coming soon😊')

side_check_button = st.sidebar.button('Check Your Essay', type=type_check, use_container_width=True)

st.sidebar.write("If you want to calculate the overall band score of Task 1 and Task 2 press the button 👇")

side_check_button2 = st.sidebar.button('Caculate overall Band Score', type=type_take, use_container_width=True)
if side_check_button2:
    st.switch_page("pages/overall.py")
    # st.page_link("pages/overall.py", label="IELTS Overall Band Score Calculater", icon="🔶")
# side_take_button = st.sidebar.button("Take a Test (it's coming soon)", type=type_take, use_container_width=True, disabled=True)


st.sidebar.write('Now you can evaluate your essay via Telegram: https://t.me/ielts_writing2_bot')
st.sidebar.write("If there is any issue in the performance or any suggetions please contact me")

st.sidebar.write("Email: mustafabinothman2023@gmail.com")
st.sidebar.write("Telegram:  https://t.me/mustafa_binothman")
st.sidebar.markdown("Developed by **Mustafa Bin Othman**")

def is_valid_gmail(email):
    gmail_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
    return gmail_regex.match(email) is not None

def check_email(email):
    try:
        with open('registered_emails.csv', 'r') as file:
            reader = csv.reader(file)
            emails = [row[0] for row in reader]
            if email in emails:
                return True
            else:
                with open('registered_emails.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([email])
                return False
    except FileNotFoundError:
        with open('registered_emails.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email])
        return False

st.title('IELTS Writing Evaluator (Free)')
st.write('This is a high-quality AI that is competent in evaluating IELTS writing. It uses advanced LLMs to make a high efficient evaluation .')

# email = st.text_input('please enter your email')
# if st.button('Rigester'):
#         if not is_valid_gmail(email):
#             st.error('Please enter a valid Gmail email.')
#         else:
#             result = check_email(email)
#             if result is True:
#                 st.success('Email already registered. You can use the website.')
#                 # Add your website functionality here
#             elif result is False:
#                 st.success('Email registered successfully. You can now use the website.')
#                 # Add your website functionality here
#             else:
#                 st.error('Invalid Gmail email. Please provide a valid Gmail address.')

task = ''
gen_acad = ''
select_task = st.selectbox('**Please Select the type of task**', ['Task 1', 'Task 2'])

if select_task == 'Task 1':
    task = 'Task 1'
    gen_aca = st.selectbox('**Academic or General essay**', ['Academic', 'General'])
    gen_acad = gen_aca
    if gen_acad == 'Academic':
        chart_image = st.file_uploader('Please upload Task 1 chart/map etc.. (optional)', type=['png', 'jpg'] )
        st.write("if you have written your essay in a paper, take a photo and upload it 👇")
        task_image= st.file_uploader('Please upload a photo of the essay', type=['png', 'jpg'] )
        st.markdown("> ✅ **Important Notes** ")
        st.markdown("**1- Make sure you upload a high quality photo with clear font for better results**")
        st.markdown("**2- After you upload the photo check the written essay and edit it if there any issues**")
        st.markdown("**3- If one photo wasn't enough to upload all the essay you can cancel the photo and upload the other photos (it will automatically add the text with first one)**")
    else:
        task_image= st.file_uploader('Please upload a photo of the essay', type=['png', 'jpg'] )
        st.markdown("> ✅ **Important Notes** ")
        st.markdown("**1- Make sure you upload a high quality photo with clear font for better results**")
        st.markdown("**2- After you upload the photo check the written essay and edit it if there any issues**")
        st.markdown("**3- If one photo wasn't enough to upload all the essay you can cancel the photo and upload the other photos (it will automatically add the text with first one)**")
    
    
else:
    task = 'Task 2'
    st.write("if you have written your essay in a paper take a photo and upload it 👇")
    
    task_image= st.file_uploader('Please upload a photo of the essay', type=['png', 'jpg'] )
    st.markdown("> ✅ **Important Notes** ")
    st.markdown("**1- Make sure you upload a high quality photo with clear font for better results**")
    st.markdown("**2- After you upload the photo check the written essay and edit it if there any issues**")
    st.markdown("**3- If one photo wasn't enough to upload all the essay, you can cancel the photo and upload the other photos (it will automatically add the text with first one)**")

opus = "claude-3-opus-20240229"
sonnet = "claude-3-sonnet-20240229"
haiku = "claude-3-haiku-20240307"
overall_band_score = []
def claude_model(model, prompt):
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=Claude_API_KEY,
        )

            message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.0,
            # system="Respond only in Yoda-speak.",
            messages=[
                {"role": "user", "content": prompt}
        ]
        )
            content_block = message.content[0]
        except Exception  as e:
            retries += 1
            print("An internal error has occurred: now will use ", e)
            print("Retrying...")
            continue
    else:
        st.error("ERORR!!!, please try again or contact me")
        
    # st.write(content_block.text)
    remove_band_score(content_block.text)
    # task_score = float(extract_digit_from_essay(content_block.text))
    # overall_band_score.append((task_score))
    

def claude_model2(model, prompt):
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=Claude_API_KEY,
        )

            message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.0,
            # system="Respond only in Yoda-speak.",
            messages=[
                {"role": "user", "content": prompt}
        ]
        )
            content_block = message.content[0]
            # st.write(content_block.text)
            return content_block.text
        except Exception  as e:
                retries += 1
                print("An internal error has occurred: now will use ", e)
                print("Retrying...")
                continue
    else:
        st.error("ERORR!!!, please try again or contact me")
        
    



        
def decripe_image(api, image):
    image_prompt = 'only describe the image and do not add any additional information that the image do not present'
    genai.configure(api_key=api)
    model_vision = genai.GenerativeModel('gemini-pro-vision')
    while True:
        try:
            response2 = model_vision.generate_content([image_prompt, image])
            response2.resolve()
            describe = response2.text
            return describe
            # print('---------------')
            # print(len(described_image))
            break
        except Exception as e:
            print("An error has occurred:", e)
            print("Retrying...")
            continue
# described_image = decripe_image()
# print (described_image)
# print('----')

describe_image = ''
if task == 'Task 1' and gen_acad == 'Academic' :
    if chart_image is not None:
        image_pil = Image.open(chart_image)
        # described_image = decripe_image(used_key, image_pil)
        # describe_image += described_image
        # print (described_image)
        # print('----')
        st.image(image_pil, width=500)
    else:
        pass
        # decripe_image(used_key, image_pil)
        

value= ''
number_of_tries = 5
def essay_image(api_key, image_pil):
    
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            image_prompt = 'Please transcribe the text from the provided image without adding any additional information or making changes to the words. Ensure accuracy in detecting and reproducing the text exactly as it appears in the image, including any spelling mistakes. Your task is to strictly adhere to the content visible in the image and refrain from introducing any extraneous details or alterations to the text.'
            genai.configure(api_key=api_key)
            model_vision = genai.GenerativeModel('gemini-pro-vision')
            response2 = model_vision.generate_content([image_prompt, image_pil])
            response2.resolve()
            describe = response2.text
            prompt_image = f"""
            You will be given text extracted from one or more images, which together should form an IELTS essay. 
            Your task is to carefully analyze the extracted text from each image, 
            ignoring any text that is not part of the essay. It is crucial that you do not make any changes to the essay's content, including correcting spelling or grammar, 
            the extracted text is {describe}
            Instructions:

            1- Read through the extracted text from each provided image, looking for the main body of the IELTS essay.

            2- Ignore any text that appears to be unrelated to the IELTS essay, such as:
                a. Headers or footers containing page numbers, dates, or other irrelevant information.
                b. Instructions or prompts related to the IELTS writing task.
                c. Personal notes or comments not intended to be part of the essay.
                d. Incomplete sentences or fragments that do not contribute to the essay's content.

            3- If there is no unrelated text in the extracted text from the image and the entire text forms a complete IELTS essay, return the essay text as-is, without adding any additional information or making any changes to the content.

            4- Do not make any changes to the essay's content, including correcting spelling, grammar, or punctuation errors. The essay should be preserved in its original form

            
            """
            response = model.generate_content(prompt_image, stream=True)
            response.resolve()
            rewrite = response.text
            return rewrite
            break
        except Exception  as e:
            retries+=1
            print("An internal error has occurred:", e)
            print("Retrying...")
            continue
    else:
        st.error('ERORR!!!, please try again')


question = st.text_area(label='**Enter the question of the essay**')
# st.markdown('### Write the essay')
if 'essay' not in st.session_state:
    st.session_state.essay = value

if 'image_processed' not in st.session_state:
    st.session_state.image_processed = False

if task_image is not None:
    if not st.session_state.image_processed or task_image != st.session_state.last_uploaded_image:
        image_pil = Image.open(task_image)
        extracted_text = essay_image(Gemini_API_Key, image_pil)
        if st.session_state.essay:
            st.session_state.essay = st.session_state.essay + '\n' + extracted_text
        else:
            st.session_state.essay = extracted_text
        st.session_state.image_processed = True
        st.session_state.last_uploaded_image = task_image



essay = st.text_area(label='**Write or paste the essay**', height=600, value=st.session_state.essay)
num_words = len(essay.split())
q_words = len(question.split())
st.write('Number of Words:    ',num_words)
button = st.button('Evaluate')

grammar_check = ''
TR_task = ''
task_resp_1_aca = ''
task_resp_1_gen = ''
coherence = ''
lexic = ''
suggeted_score = ''



list_of_repeated_words = []
number_of_tries = 5

# functions
def words_charts():
    from collections import Counter

    # Remove punctuation and convert to lowercase
    essay_cleaned = re.sub(r'[^\w\s]', '', essay).lower()

    excluded_words = ['who','were','it','of','the','it','from','was','my','these', 'your', 'you', 'this', 'because', 'other', 'before', 'after', 'should', 'would', 'can', 'be', 'why', 'where', 'when', 'what', "don't", 'does', 'do', 'how', 'which', 'that', 'me', 'am', 'i', "hasn't", "havn't", 'we', 'they', 'she', 'he', 'us', 'our', 'its', 'their', 'them', 'her', 'him', 'his', 'while', 'it', 'while', 'about', 'are', 'is', 'has', 'have', 'at', 'in', 'on', 'of', 'to', 'from', 'for', 'with', 'by', 'as', 'and', 'or', 'but', 'nor', 'so', 'yet', 'the', 'a', 'an', 'not','afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda', 'argentina', 'armenia', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'central african republic', 'chad', 'chile', 'china', 'colombia', 'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'eswatini', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'honduras', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'north korea', 'north macedonia', 'norway', 'oman', 'pakistan', 'palau', 'palestine', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south korea', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'sweden', 'switzerland', 'syria', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe', 'africa', 'antarctica', 'asia', 'europe', 'north america', 'south america', 'australia', 'states', 'united','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # countries_and_continents = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda', 'argentina', 'armenia', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'central african republic', 'chad', 'chile', 'china', 'colombia', 'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'eswatini', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'honduras', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'north korea', 'north macedonia', 'norway', 'oman', 'pakistan', 'palau', 'palestine', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south korea', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'sweden', 'switzerland', 'syria', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe', 'africa', 'antarctica', 'asia', 'europe', 'north america', 'south america', 'australia', 'states', 'united',]

    # Split the essay into words and exclude words in the excluded_words list
    words = [word for word in essay_cleaned.split() if word not in excluded_words]
    # words = [word for word in essay_cleaned.split() if word not in countries_and_continents]
    # Filter out numbers from the words list
    words = [word for word in words if not word.isdigit()]

    word_counts = Counter(words)
    most_repeated_words = word_counts.most_common(5)

    for word, count in most_repeated_words:
        list_of_repeated_words.append(word)

    st.markdown('**Top 5 Most Repeated Words**')

    words = [word for word, _ in most_repeated_words]
    counts = [count for _, count in most_repeated_words]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Top 5 Most Repeated Words')
    st.pyplot(plt)
def organaize_synonyms(api, synonyms):
    sy_prompt = f"""
    
    you will be given a list of words with their synonyms and your task is to organaize them and make them in markdown format
    and i want it like this format  below
    the synonyms are: {synonyms}
    
    **the word:**

    - Synonym 1
    - Synonym 2
    - Synonym 3
    
    

    
    """
    
    
    genai.configure(api_key = api)
    # model = genai.GenerativeModel('gemini-1.0-pro-latest')
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            # claude_model2(haiku, sy_prompt)
            response2 = model.generate_content(sy_prompt, stream=True)
            response2.resolve()
            synonyms = response2.text
            st.markdown(synonyms)
            break  # Break out of the while loop if the generation is successful
        except Exception as e:
            print("An error has occurred:", e)
            print("Retrying...")
            continue
    else:
        st.error('Error') 
def synonym(api):
#     sy_prompt = f"""Please provide three synonyms for each of the five words I will give you,
#     closely related to the meaning of the word in the context of this essay {essay}. Your response should include words suitable for IELTS writing 
#     to enhance the score and should avoid repeating the same word. The words should be 100% related to the intended meaning 
#     in the context of the word from the provided IELTS writing essay. Please list the words followed by their synonyms in order,
#     without any additional information unrelated to the task. please if the synonym is not suitable for the context of the word do not write it 
# The words are {list_of_repeated_words} from the IELTS writing essay {essay}.
# and you should organize them 
#     """
    
    sy_prompt = f"""As an English language expert, your task is to provide three context-appropriate synonyms for each of the five words given from an IELTS writing essay from this repeated words {list_of_repeated_words} in this essay {essay}. 
    The synonyms should be carefully chosen to maintain the intended meaning of the words within the essay's context and to enhance the writing score. 
    Avoid repeating the same word or suggesting synonyms that do not fit the context. 
    
    Instructions:

    1- Review the provided IELTS writing essay and the list of five repeated words.

    2- For each word, provide three synonyms that are suitable for the word's intended meaning within the essay's context.

    3- Ensure that the suggested synonyms are appropriate for IELTS writing and can help enhance the writing score.

    4- Present the synonyms in the following format:
    Word 1:

    Synonym 1
    Synonym 2
    Synonym 3
    Word 2:

    Synonym 1
    Synonym 2
    Synonym 3
    (Repeat the format for all five words)

    5- If a word has no suitable synonyms that fit the context, skip that word and move on to the next one.

    Remember to focus solely on providing context-appropriate synonyms without including any additional information unrelated to the task.
    """
    
    
    genai.configure(api_key = api)
    # model = genai.GenerativeModel('gemini-1.0-pro-latest')
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            # claude_model2(haiku, sy_prompt)
            response2 = model.generate_content(sy_prompt, stream=True)
            response2.resolve()
            synonyms = response2.text
            organaize_synonyms(api, synonyms)
            break  # Break out of the while loop if the generation is successful
        except Exception as e:
            print("An error has occurred:", e)
            print("Retrying...")
            continue
    else:
        st.error('Error') 
def rewrite_essay(api):
    # re_prompt = f"""
    # pretend you are English teacher and you have experience in IELTS writing essays 
    # your task is to rewrite this IELTS writing essay {essay} based on this question {question}to a better version and match 
    # IELTS requirements in IELTS academic writing {task}, please do not write the headline of the paragraph
    # and it must be more than 250 words and less than 330 words if task 2 and more than 150 and less than 200 if task 1
    
    # In your revised essay, focus on refining the structure, coherence, and language to meet the IELTS academic writing standards. Ensure that the essay effectively addresses the question, 
    # demonstrates a clear understanding of the topic, and presents well-developed ideas with supporting examples and evidence. Additionally, pay attention to grammar, vocabulary, 
    # and sentence structure to create a more polished and coherent essay that meets the requirements for IELTS academic writing.
    # """
    
    re_prompt = f"""
    As an experienced IELTS writing teacher, your task is to rewrite the given IELTS writing essay {essay} based on the provided question {question}, ensuring that it meets the IELTS academic writing requirements for the specified task {task}. The revised essay should focus on refining the structure, coherence, and language while effectively addressing the question and presenting well-developed ideas with supporting examples and evidence.

    Instructions:

    Carefully review the given IELTS writing essay, question, and the specified task (Task 1 or Task 2).
    Analyze the essay's structure, coherence, and language, identifying areas that need improvement to meet IELTS academic writing standards.
    Rewrite the essay, focusing on the following aspects:
    a. Ensure that the essay effectively addresses the question and demonstrates a clear understanding of the topic.
    b. Present well-developed ideas with supporting examples and evidence.
    c. Improve the essay's structure and coherence, ensuring a logical flow of ideas and smooth transitions between paragraphs.
    d. Refine the language, paying attention to grammar, vocabulary, and sentence structure to create a more polished and coherent essay.
    Ensure that the revised essay meets the word count requirements:
    For Task 2: The essay must be more than 250 words and less than 330 words.
    For Task 1: The essay must be more than 150 words and less than 200 words.
    Do not include the headline of the paragraph in the revised essay.
    Remember to focus on creating a revised essay that meets the IELTS academic writing standards and effectively addresses the given question while staying within the specified word count range and do not write the count of words in your rewrite essay.
    
    """
    
    genai.configure(api_key = api)
    # model = genai.GenerativeModel('gemini-1.0-pro-latest')
    
    num_word = 0
    if task == 'Task 1':
        num_word = 150
    else:
        num_word = 250
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            while True:
                response = model.generate_content(re_prompt, stream=True)
                response.resolve()
                rewrtie = response.text
                word_count = len(rewrtie.split())
                
                if word_count >= num_word and word_count < (num_word + 40):
                    st.write(rewrtie)
                    st.write('Number of Words:', word_count)
                    # print("Essay generated successfully.")
                    print(num_word)
                    break  # Break out of the loop if the essay meets the word count requirement
                else:
                    # print("The generated essay is under 250 words. Regenerating...")
                    continue 
            break  # Break out of the while loop if the generation is successful
        except Exception as e:
            print("An error has occurred:", e)
            print("Retrying...")
            continue
    else:
        print("Maximum retries reached. Switching to claude_model.")
        while True:
            client = anthropic.Anthropic(api_key=Claude_API_KEY,)
            message = client.messages.create(
            model=haiku,
            max_tokens=1000,
            temperature=0.0,
            # system="Respond only in Yoda-speak.",
            messages=[
                {"role": "user", "content": re_prompt}
        ]
        )
            content_block = message.content[0]
            re_write = content_block.text
            word_count = len(re_write.split())
                
            if word_count >= num_word and word_count < (num_word + 40):
                    st.write(re_write)
                    st.write('Number of Words:', word_count)
                    # print("Essay generated successfully.")
                    print(num_word)
                    break  # Break out of the loop if the essay meets the word count requirement
            else:
                    # print("The generated essay is under 250 words. Regenerating...")
                    continue 
          # Break out o
def count_words():
    more_details = st.button('more details')
    if more_details:
        st.markdown('##Here are the most repeated words in your essay')
        stop_w = set(STOPWORDS)
        #words = essay
        word_cloud = WordCloud(stopwords=stop_w).generate(essay)
        img = word_cloud.to_image()
        st.image(img)    
def grammar_spelling():
    
    prompt = f"""
    As an advanced grammar checker, your task is to meticulously review the provided essay {essay} and identify any misspelled words and grammatical errors. Provide accurate corrections and clear explanations to help the writer understand and improve their language usage.

Instructions:

Carefully read through the essay, focusing on identifying misspelled words and grammatical errors.

For misspelled words:
a. Provide the correct spelling of the word.
b. Consider both British and American English conventions when providing the correct spelling.
c. If a word is correctly spelled but used incorrectly in the context, provide an explanation and suggest a more appropriate word if necessary.

For grammatical errors:
a. Highlight the specific part of the sentence or phrase that contains the grammatical error.
b. Provide the correct grammar structure.
c. Explain why the provided correction is accurate and how it improves the language usage in the essay.
d. If the error involves a complex grammar rule, provide a concise explanation to help the writer understand the underlying principle. Consider including links to reputable grammar resources or specific exercises to practice the identified areas of improvement.

Be cautious not to identify correctly spelled words as misspellings. Focus only on actual misspelled words to avoid confusing the writer.

If there are no misspelling mistakes or grammatical errors, provide a positive acknowledgment, such as: "Great job! Your grammar and spelling are accurate throughout the essay."

Maintain a supportive and encouraging tone in your feedback. Provide constructive suggestions and explanations that motivate the writer to continue improving their language skills.

Focus on providing accurate corrections and explanations without rewriting the entire essay. Your feedback should help the writer understand their mistakes and learn how to improve their language usage.

If you encounter an error that you are unsure about, it's better to skip it rather than provide an incorrect correction. Prioritize accuracy over identifying every potential error.

If the essay contains recurring errors or patterns, provide a more detailed explanation of the underlying grammar rule to help the writer avoid making the same mistakes in the future.

If the essay has a few awkward or unclear sentences that don't necessarily contain grammatical errors, provide suggestions on how to rephrase them for better clarity and coherence.

After completing your review, provide a brief summary of the most common types of errors found in the essay, if any. This will help the writer identify patterns and areas for improvement.

if there are no misspelling mistakes or incorrect grammar you should write your grammar and spelling is correct

Remember, your goal is to provide accurate, helpful, and constructive feedback that enables the writer to enhance their grammar and spelling skills in the context of IELTS essay writing.
    """
    # def function_reviwer(gra_spelling):
    #     reviwer_prompt = f"""
    #     You are an AI reviewer. Your task is to monitor the output of another AI called the Grammar and Spelling Checker. The Grammar and Spelling Checker's task is to review an IELTS writing essay and identify any misspellings or incorrect grammar usage.

    #     Sometimes the Grammar and Spelling Checker makes mistakes, such as:
    #     - Providing incorrect corrections
    #     - Giving wrong information
    #     - Rewriting the essay instead of focusing on corrections and explanations

    #     Here is the output from the Grammar and Spelling Checker:
    #     {gra_spelling}

    #     Please review the output and provide the following:
    #     1. Correct any mistakes made by the Grammar and Spelling Checker in identifying misspellings or grammar errors.
    #     2. Remove any unnecessary rewriting of the essay and focus only on providing accurate corrections and explanations.
    #     3. Improve the explanations and corrections provided by the Grammar and Spelling Checker, if needed, to make them clearer and more helpful for the writer.
    #     """
    #     task = model.generate_content(reviwer_prompt, stream=True)
    #     task.resolve()
    #     task_ch = task.text
    #     st.write(task_ch)
    #     print(task_ch)
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            # gra_spelling = claude_model2(haiku, prompt)
            genai.configure(api_key = used_key)
            task = model.generate_content(prompt, stream=True)
            task.resolve()
            task_ch = task.text
            st.write(task_ch)
            # function_reviwer(task_ch)
            
            break  # Break out of the while loop if the generation is successful
        except Exception  as e:
            retries+=1
            print("An internal error has occurred:", e)
            print("Retrying...")
            continue
    else:
        claude_model2(haiku, prompt) 
def grammar_spelling2():

    prompt = f"""
    As an advanced grammar checker, your task is to meticulously review the provided essay {essay} and identify any misspelled words and grammatical errors. Provide accurate corrections and clear explanations to help the writer understand and improve their language usage.

        Instructions:

        Carefully read through the essay, focusing on identifying misspelled words and grammatical errors.

        For misspelled words:
        a. Provide the correct spelling of the word.
        b. Consider both British and American English conventions when providing the correct spelling.
        c. If a word is correctly spelled but used incorrectly in the context, provide an explanation and suggest a more appropriate word if necessary.

        For grammatical errors:
        a. Highlight the specific part of the sentence or phrase that contains the grammatical error.
        b. Provide the correct grammar structure.
        c. Explain why the provided correction is accurate and how it improves the language usage in the essay.
        d. If the error involves a complex grammar rule, provide a concise explanation to help the writer understand the underlying principle. Consider including links to reputable grammar resources or specific exercises to practice the identified areas of improvement.

        Be cautious not to identify correctly spelled words as misspellings. Focus only on actual misspelled words to avoid confusing the writer.

        If there are no misspelling mistakes or grammatical errors, provide a positive acknowledgment, such as: "Great job! Your grammar and spelling are accurate throughout the essay."


        Focus on providing accurate corrections without rewriting the entire essay. 

        If you encounter an error that you are unsure about, it's better to skip it rather than provide an incorrect correction. Prioritize accuracy over identifying every potential error.


        After completing your review, provide a brief summary of the most common types of errors found in the essay, if any. This will help the writer identify patterns and areas for improvement.

        if there are no misspelling mistakes or incorrect grammar you should write your grammar and spelling is correct

        Remember, your goal is to provide accurate, helpful, and constructive feedback that enables the writer to enhance their grammar and spelling skills in the context of IELTS essay writing.
    """
    
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            # gra_spelling = claude_model2(haiku, prompt)
            genai.configure(api_key = used_key)
            task = model.generate_content(prompt, stream=True)
            task.resolve()
            task_ch = task.text
            # st.write(task_ch)
            return task_ch
            # function_reviwer(task_ch)
            
            break  # Break out of the while loop if the generation is successful
        except Exception  as e:
            retries+=1
            print("An internal error has occurred:", e)
            print("Retrying...")
            continue
    else:
        claude_model2(haiku, prompt)
        # max_retries = number_of_tries
        # retries = 0
        # while True:
        #     try:
        #         client = anthropic.Anthropic(
        #     # defaults to os.environ.get("ANTHROPIC_API_KEY")
        #         api_key=Claude_API_KEY,
        #     )

        #         message = client.messages.create(
        #         model=model,
        #         max_tokens=1000,
        #         temperature=0.0,
        #         # system="Respond only in Yoda-speak.",
        #         messages=[
        #             {"role": "user", "content": prompt}
        #     ]
        #     )
        #         content_block = message.content[0]
        #         # st.write(content_block.text)
        #         return content_block.text
        #         break
        #     except Exception  as e:
        #             retries += 1
        #             print("An internal error has occurred: now will use ", e)
        #             print("Retrying...")
        #             continue
        # else:
        #     st.error("ERORR!!!, please try again or contact me")
def essay_analysis(prompt):

    genai.configure(api_key = used_key)
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            for _ in range(2):
                task = model.generate_content(prompt, stream=True)
                task.resolve()
                task_ch = task.text
                # print(task_ch)
                # print('-----------------------------')
                # print("1")
                return task_ch
                
        #    --------------------------
#             
            break  # Break out of the while loop if the generation is successful
        except Exception  as e:
            retries += 1
            print("An internal error has occurred: now will use ", e)
            print("Retrying...")
            continue
        
    else:
        client = anthropic.Anthropic(
# defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=Claude_API_KEY,
        )

        message = client.messages.create(
        model=haiku,
        max_tokens=1000,
        temperature=0.0,
            # system="Respond only in Yoda-speak.",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        content_block = message.content[0]
        return content_block.text    
def suggested_score_ana(task_analysis, task):
    
    
    prompt = f"""
    
    i will give you a paragrph for ielts writing essay {task} analysis and i want you to only search about the suggested band score that in the paragrpah
    and then write the suggested band score and its justification the is provided also in the paragraph
    the paragraph is {task_analysis} you should be extermly accurate 

    
    """
    
    genai.configure(api_key = used_key)
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            task = model.generate_content(prompt, stream=True)
            task.resolve()
            task_ch = task.text
            # print('-------------&---------------')
            # print('-------------&---------------')
            # print(task_ch)
            # print('-------------&---------------')
            # print('-------------&---------------')
            # print("1")
            return task_ch
            
        #    --------------------------
#             
            break  # Break out of the while loop if the generation is successful
        except Exception  as e:
            retries += 1
            print("An internal error has occurred: now will use ", e)
            print("Retrying...")
            continue

#prompts
# task response criteria prompt
tr_task2_analysis = f"""

    You are an IELTS writing assistant tasked with detecting errors and mistakes in IELTS Writing {task} essays. Your primary focus is to identify and categorize the errors found in the essay to help the main evaluating function provide a reliable band score for the Task Response criterion.

    After carefully reviewing the essay text {essay}, generate a comprehensive report that lists and categorizes the errors and mistakes found in the essay. Provide specific examples from the essay to support your observations.

    The goal is to produce a consistent and reliable report that can assist the main evaluating function in determining an accurate band score for the essay's Task Response based on the IELTS Writing {task} criteria.

    Report Structure:

    Task Fulfillment Errors:

    - Identify any errors related to task fulfillment, such as failing to address all parts of the task, irrelevance, or inadequate development of position.
    - Provide a clear count of the total number of task fulfillment errors found in the essay.
    - Include specific examples of task fulfillment errors from the essay.
    
    and also consider these terms carfully
    - Addressing all parts of the task adequately
    - Presenting a clear position or overview
    - Supporting ideas with relevant explanations and examples
    - Fully developing the topic within the given word count
    
    if the question has two parts, such as "discuss both views and give your own opinion," and this is the question of the essay {question} 
    the candidate must address both parts adequately. If they only discuss one view or fail to provide their opinion, their Task Response score will suffer. Additionally, 
    if the candidate misinterprets the question or provides irrelevant information, it will negatively affect their score.
    
    
    Coherence and Cohesion Errors:

    - Identify any errors related to coherence and cohesion, such as lack of logical flow, inadequate use of cohesive devices, or poor paragraph organization.
    - Provide a clear count of the total number of coherence and cohesion errors found in the essay.
    - Include specific examples of coherence and cohesion errors from the essay.
    
    Lexical Errors:

    - Identify any errors related to vocabulary usage, such as inaccurate word choice, spelling mistakes, or inappropriate word formation.
    - Provide a clear count of the total number of lexical errors found in the essay.
    - Include specific examples of lexical errors from the essay.
    
    Grammatical Errors:

    - Identify any errors related to grammar, such as subject-verb agreement, verb tense, article usage, or sentence structure issues.
    - Provide a clear count of the total number of grammatical errors found in the essay.
    - Include specific examples of grammatical errors from the essay.
    
    Other Errors:

    - Identify any other errors or mistakes that do not fit into the above categories, such as punctuation or formatting issues.
    - Provide a clear count of the total number of other errors found in the essay.
    - Include specific examples of other errors from the essay.
    
    Total Error Count:

    Provide the total count of all errors and mistakes identified in the essay.
    Error Severity:

    Assess the severity of the identified errors and their potential impact on the essay's overall quality and comprehensibility.
    Categorize the errors as minor, moderate, or severe based on their frequency and impact on the essay's effectiveness.
    
    Please provide a detailed and objective analysis of the essay's errors and mistakes, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations.
    Suggested Band Score:

        Provide a suggested band score for the essay based on the following criteria:
        If the essay contains significant errors (more than 10) and lacks coherence, suggest a score between 3 and 5, and provide a specific score with justification.
        If the essay is well-written, addresses the task effectively, and contains only minor errors (fewer than 5), suggest a score between 6 and 9, and provide a specific score with justification.
        Support the suggested band score by referencing specific strengths and weaknesses identified in the report, as well as the error count.
        Please provide a detailed and objective analysis of the essay, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations and provide constructive suggestions for improvement in each area. Be precise in your analysis and ensure that all mistakes and areas needing improvement are addressed.

    To use the generated report in assisting the main evaluating function:

    1- Carefully review the report, noting the identified errors, their categorization, and the provided examples from the essay.
    2- Consider the total error count and the severity of the errors in relation to the IELTS Writing {task} Task Response band descriptors.
    3- Use the insights from the report to guide the evaluation of the essay's performance in the Task Response criterion.
    4- Ensure consistency in the evaluation by referring to the report's findings and the official IELTS Writing {task} Response band descriptors.

"""
tas_prompt= f"""
You are an IELTS examiner and your role is to assess IELTS Writing Essays. In this task {task}, your focus is to evaluate only the TASK RESPONSE of the given essay {essay} based on the official Task Response assessment criteria provided by IELTS.org.

 to help you while evaluating i created  analysis tool that can first before your evalation make an intial evalaution of the aimed essay 
        and this will guide you to the most significant mistakes and errors are existed in the essay that might affect the finall score of task response
        and this will give you the confidence that you make an efficiant evalaution 
        
        and you should use this analysis in your assessment and take all the time you need the most important thing is provide a reliable score for the citeria
    important Note:
        in the analysis based on the mistakes are in the essay it will provide a suggetion of the score that might be lower than yours please you should consider that 
        and that might mean that your evaluation was inaccurate and you then will mislead the ielts taker who is rely on you 
        so please make sure you do not be misleader for them and i created this tool because i want you to be the best so please consider this effort
        
        now i will give you the result of the analysis and make as a guide for you trust me it will give you things will diffentely help you
        this is the analysis of the essay {TR_task} also to further helping you this is a grammar chacker that i also created 
        to help you know the most mistakes that the writer made in his eesay and i want you to use it in your evalaution 
        this is the analysis of the grammar {grammar_check}
        
        and to make it is to you to decide the deserved score which i am confident you will do that here is the suggested band score that the tool estimated for you because it wants helping you {suggeted_score}
        
        i hope you will not let me down and use what i told you above 

Instructions for assessing Task Response:
For {task} of both AC Writing tests, candidates are required to formulate and 
    develop a position in relation to a given prompt in the form of a question or 
    statement, using a minimum of 250 words and the number of words that the candidate has been written is {num_words}. if it is more than 320 it is a bad thing
    Ideas should be supported by evidence, 
    and examples may be drawn from a candidate’s own experience.
    
    TASK RESPONSE (TR) 
    The TR criterion assesses:
    
    - how fully the candidate responds to the task.
    - how adequately the main ideas are extended and supported. 
    - how relevant the candidate’s ideas are to the task. 
    - how clearly the candidate opens the discourse, establishes their position and formulates conclusions. 
    - how appropriate the format of the response is to the task.
    
    and also consider these terms carfully
    - Addressing all parts of the task adequately
    - Presenting a clear position or overview
    - Supporting ideas with relevant explanations and examples
    - Fully developing the topic within the given word count
    
    if the question has two parts, such as "discuss both views and give your own opinion," and this is the question of the essay {question} 
    the candidate must address both parts adequately. If they only discuss one view or fail to provide their opinion, their Task Response score will suffer. Additionally, 
    if the candidate misinterprets the question or provides irrelevant information, it will negatively affect their score.
    
    Be objective and unbiased in your assessment, ensuring that your evaluation is based solely on the IELTS criteria and not influenced by the essay's topic, stance, or the candidate's language background.

Band descriptors for the TR criterion:
    Band 9: The prompt is appropriately addressed and explored in depth. A clear and fully developed position is presented which directly answers the question/s. Ideas are relevant, fully extended and well supported. Any lapses in content or support are extremely rare.

    Band 8: The prompt is appropriately and sufficiently addressed. A clear and well-developed position is presented in response to the question/s. Ideas are relevant, well extended and supported. There may be occasional omissions or lapses in content.
    
    Band 7: The main parts of the prompt are appropriately addressed. A clear and developed position is presented. Main ideas are extended and supported but there may be a  tendency to over-generalise or there may be a lack of focus and  precision in supporting ideas/material.
        
    Band 6: The main parts of the prompt are addressed (though some may be more fully covered than others). An appropriate format is used. A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive. Main ideas are relevant, but some may be insufficiently developed or may lack clarity, while some supporting arguments and evidence may be less relevant or inadequate.
        
    Band 5: The main parts of the prompt are incompletely addressed. The format may be inappropriate in places. The writer expresses a position, but the development is not always clear. Some main ideas are put forward, but they are limited and are not sufficiently developed and/or there may be irrelevant detail. There may be some repetition.
        
    Band 4: The prompt is tackled in a minimal way, or the answer istangential, possibly due to some misunderstanding of the prompt. The format may be inappropriate. A position is discernible, but the reader has to read carefullyto find it. Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support. Large parts of the response may be repetitive.
        
    Band 3: No part of the prompt is adequately addressed, or the prompt has been misunderstood. No relevant position can be identified, and/or there is little direct response to the question/s. There are few ideas, and these may be irrelevant or insufficiently developed
        
    Band 2: The content is barely related to the prompt. No position can be identified. There may be glimpses of one or two ideas without development.
        
    Band 1: Responses of 20 words or fewer are rated at Band 1. The content is wholly unrelated to the prompt. An co ied rubric must be discounted.

    Band 0: The candidate did not attempt the task, so no assessment of task response can be made.
     

Structure your response as follows:

Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

Evaluation: To guide your evaluation, follow these steps:
1- Carefully review the essay prompt and the candidate's response.
2- Analyze how well the candidate addresses all parts of the prompt. Consider the relevance and clarity of the presented position, main ideas, and supporting examples.
3- Evaluate the development and extension of the main ideas. Are they sufficiently explained and supported with relevant examples or evidence?
4- Assess the coherence and cohesion of the response. Is there a logical flow of ideas, with clear connections between paragraphs?
5- Determine the band score (1-9) for Task Response based on the official IELTS band descriptors. Provide a brief justification for your score.
6- Identify 2-3 specific strengths of the essay's Task Response, providing examples from the text to support your points.
7- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Task Response.
8- Comment on the essay's adherence to the minimum word count (250 words) and how it impacts the Task Response. If the essay is under the word count, suggest ways to expand the content.
9- Provide an overall assessment of the essay's Task Response, highlighting the main takeaways and offering encouragement for future improvement.

Please note that your evaluation should be unbiased and based solely on the IELTS Task Response criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.

Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS writing skills and achieve their desired band score.
"""


# coherence and cohision criteria prompt
co_task2_analysis = f"""

    You are an IELTS writing assistant tasked with detecting errors and issues related to Coherence and Cohesion in IELTS Writing {task} essays. Your primary focus is to identify and categorize the Coherence and Cohesion issues found in the essay to help the main evaluating function provide a reliable band score for the Coherence and Cohesion criterion.

        After carefully reviewing the essay text {essay}, generate a comprehensive report that lists and categorizes the Coherence and Cohesion errors and issues found in the essay. Provide specific examples from the essay to support your observations.

        The goal is to produce a consistent and reliable report that can assist the main evaluating function in determining an accurate band score for the essay's Coherence and Cohesion based on the IELTS Writing {task} criteria.

        Report Structure:

        Overall Essay Structure:

        - Assess the overall structure and organization of the essay.
        - Identify any issues related to the introduction, body paragraphs, and conclusion.
        - Provide a clear count of the total number of essay structure issues found in the essay.
        - Include specific examples of essay structure issues from the essay.
        
        Paragraph Organization:

        - Evaluate the organization and structure of individual paragraphs in the essay.
        - Identify any issues related to topic sentences, supporting details, or concluding sentences.
        - Provide a clear count of the total number of paragraph organization issues found in the essay.
        - Include specific examples of paragraph organization issues from the essay.
        
        Logical Sequencing and Progression:

        - Assess the logical sequencing and progression of ideas within and between paragraphs.
        - Identify any instances where the flow of ideas is illogical, disjointed, or hard to follow.
        - Provide a clear count of the total number of logical sequencing and progression issues found in the essay.
        - Include specific examples of logical sequencing and progression issues from the essay.
        
        Linking Devices and Cohesive Mechanisms:

        - Evaluate the use of linking devices (e.g., connectives, transitional phrases) and cohesive mechanisms (e.g., referencing, substitution) in the essay.
        - Identify any instances of missing, inappropriate, or overused linking devices or cohesive mechanisms.
        - Provide a clear count of the total number of linking device and cohesive mechanism issues found in the essay.
        - Include specific examples of linking device and cohesive mechanism issues from the essay.
        
        Repetition and Redundancy:

        - Identify instances of unnecessary repetition or redundancy that affect the coherence and cohesion of the essay.
        - Provide a clear count of the total number of repetition and redundancy issues found in the essay.
        - Include specific examples of repetition and redundancy issues from the essay.
     
    if the question has two parts, such as "discuss both views and give your own opinion," and this is the question of the essay {question} 
    the candidate must address both parts adequately. If they only discuss one view or fail to provide their opinion, their Task Response score will suffer. Additionally, 
    if the candidate misinterprets the question or provides irrelevant information, it will negatively affect their score.
    
        Total Coherence and Cohesion Issue Count:

        Provide the total count of all Coherence and Cohesion issues identified in the essay.
        Severity of Coherence and Cohesion Issues:

        Suggested Band Score:

        Provide a suggested band score for the essay based on the following criteria:
        If the essay contains significant errors (more than 10) and lacks coherence, suggest a score between 3 and 5, and provide a specific score with justification.
        If the essay is well-written, addresses the task effectively, and contains only minor errors (fewer than 5), suggest a score between 6 and 9, and provide a specific score with justification.
        Support the suggested band score by referencing specific strengths and weaknesses identified in the report, as well as the error count.
        Please provide a detailed and objective analysis of the essay, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations and provide constructive suggestions for improvement in each area. Be precise in your analysis and ensure that all mistakes and areas needing improvement are addressed.

        Assess the severity of the identified Coherence and Cohesion issues and their potential impact on the essay's overall quality and comprehensibility.
        Categorize the issues as minor, moderate, or severe based on their frequency and impact on the essay's effectiveness.
        Please provide a detailed and objective analysis of the essay's Coherence and Cohesion errors and issues, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations.

        To use the generated report in assisting the main evaluating function:

        1- Carefully review the report, noting the identified Coherence and Cohesion issues, their categorization, and the provided examples from the essay.
        2- Consider the total issue count and the severity of the issues in relation to the IELTS Writing {task} Coherence and Cohesion band descriptors.
        3- Use the insights from the report to guide the evaluation of the essay's performance in the Coherence and Cohesion criterion.
        4- Ensure consistency in the evaluation by referring to the report's findings and the official IELTS Writing {task} Coherence and Cohesion band descriptors.
"""
co_prompt = f"""
    You are an IELTS examiner and your role is to assess IELTS Writing Essays. In this task {task}, your focus is to evaluate only the COHERENCE AND COHESION of the given essay {essay} based on the official COHERENCE AND COHESION assessment criteria provided by IELTS.org.
 to help you while evaluating i created  analysis tool that can first before your evalation make an intial evalaution of the aimed essay 
        and this will guide you to the most significant mistakes and errors are existed in the essay that might affect the finall score of task response
        and this will give you the confidence that you make an efficiant evalaution 
        
        and you should use this analysis in your assessment and take all the time you need the most important thing is provide a reliable score for the citeria
    important Note:
        in the analysis based on the mistakes are in the essay it will provide a suggetion of the score that might be lower than yours please you should consider that 
        and that might mean that your evaluation was inaccurate and you then will mislead the ielts taker who is rely on you 
        so please make sure you do not be misleader for them and i created this tool because i want you to be the best so please consider this effort
        
        now i will give you the result of the analysis and make as a guide for you trust me it will give you things will diffentely help you
        this is the analysis of the essay {coherence} also to further helping you this is a grammar chacker that i also created 
        to help you know the most mistakes that the writer made in his eesay and i want you to use it in your evalaution 
        this is the analysis of the grammar {grammar_check}
        
        and to make it is to you to decide the deserved score which i am confident you will do that here is the suggested band score that the tool estimated for you because it wants helping you {suggeted_score}
        
        i hope you will not let me down and use what i told you above 
    Instructions for assessing COHERENCE AND COHESION:
    COHERENCE AND COHESION (CC) 
    This criterion is concerned with the overall organisation and logical development of 
    the message: how the response organises and links information, ideas and language. 
    Coherence refers to the linking of ideas through logical sequencing, while cohesion 
    refers to the varied and appropriate use of cohesive devices (e.g. logical connectors, 
    conjunctions and pronouns) to assist in making clear the relationships between and 
    within sentences.
    
    The CC criterion assesses: 
    - the coherence of the response via the logical organisation of information 
      and/or ideas,   or the logical progression of the argument.
    - the appropriate use of paragraphing for topic organisation and presentation.
    - the logical sequencing of ideas and/or information within and across 
      paragraphs.
    - the flexible use of reference and substitution (e.g. definite articles, pronouns). 
    - the appropriate use of discourse markers to clearly mark the stages in a 
      response, e.g. [First of all | In conclusion], and to signal the relationship between 
      ideas and/or information, e.g. [as a result | similarly]
      
    also consider this terms carfully:
    - Organizing information logically and clearly
    - Using appropriate paragraphing to group related ideas
    - Employing a range of cohesive devices (e.g., linking words, referencing) to connect ideas smoothly
    - Maintaining a clear progression throughout the essay
    
    if the question has two parts, such as "discuss both views and give your own opinion," and this is the question of the essay {question} 
    the candidate must address both parts adequately. If they only discuss one view or fail to provide their opinion, their Task Response score will suffer. Additionally, 
    if the candidate misinterprets the question or provides irrelevant information, it will negatively affect their score.
    
        
    Be objective and unbiased in your assessment, ensuring that your evaluation is based solely on the IELTS criteria and not influenced by the essay's topic, stance, or the candidate's language background.

    Below are the band descriptors for the CC criterion:
    
    Band 9: The message can be followed effortlessly. Cohesion is used in such a way that it very rarely attracts attention. Any lapses in coherence or cohesion are minimal. Paragraphing is skilfully managed.
    
    Band 8: The message can be followed with ease. Information and ideas are logically sequenced, and cohesion is well managed. Occasional lapses in coherence and cohesion may occur. Paragraphing is used sufficiently and appropriately.
        
    Band 7: Information and ideas are logically organised, and there is a clear progression throughout the response. (A few lapses may occur, but these are minor.) A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some over/under use. Paragraphing is generally used effectively to support overall coherence, and the sequencing of ideas within a paragraph is generally logical.
        
    Band 6: Information and ideas are generally arranged coherently and there is a clear overall progression. Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission. The use of reference and substitution may lack flexibility or clarity and result in some repetition or error. Paragraphing may not always be logical and/or the central topic may not always be clear.
        
    Band 5: Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response. The relationship of ideas can be followed but the sentences are not fluently linked to each other. There may be limited/overuse of cohesive devices with some inaccuracy. The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution. Paragraphing may be inadequate or missin
        
    Band 4: Information and ideas are evident but not arranged coherently and there is no clear progression within the response. Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive. There is inaccurate use or a lack of substitution or referencing. There may be no paragraphing and/or no clear main topic within paragraphs.
    
    Band 3: There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other. There is minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship ideas. There is difficulty in identifying referencing. An attem tsat ara ra hin are unhelpful.
        
    Band 2: There is little relevant message, or the entire response may be off-topic. There is little evidence of control of organisational features.
        
    Band 1: Responses of 20 words or fewer are rated at Band 1. The writing fails to communicate any message and appears to be by a virtual non-writer.
    
    Band 0: The candidate did not attempt the task, so no assessment of coherence and cohesion can be made.
   
   
   
    Structure your response as follows:

Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

Evaluation: To guide your evaluation, follow these steps:
1- Carefully review the essay prompt and the candidate's response.
2- Analyze the organization of information in the response. Is there a clear overview statement and a logical progression of ideas?
3- Evaluate the use of cohesive devices (e.g., linking words, pronouns, synonyms) to connect ideas within and between sentences and paragraphs. Are they used effectively and appropriately?
4- Assess the clarity and ease of understanding throughout the response. Is the information presented in a way that is easy to follow and comprehend?
5- Determine the band score (1-9) for Coherence and Cohesion based on the official IELTS band descriptors. Provide a brief justification for your score.
6- Identify 2-3 specific strengths of the response's Coherence and Cohesion, providing examples from the text to support your points.
7- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Coherence and Cohesion.
8- Comment on the response's adherence to the suggested paragraph structure for Academic Writing Task 2 (e.g., introduction, overview, body paragraphs) and how it impacts the Coherence and Cohesion.
9- Provide an overall assessment of the response's Coherence and Cohesion, highlighting the main takeaways and offering encouragement for future improvement.

Please note that your evaluation should be unbiased and based solely on the IELTS coherence and cohesion criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.
    
Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS  Writing {task} skills and achieve their desired band score.
    """
# lexical resources citeria prompt
lex_task2_analysis = f"""

    You are an IELTS writing assistant tasked with detecting errors and mistakes in the lexical resources of IELTS Writing {task} essays. Your primary focus is to identify and categorize the lexical errors found in the essay to help the main evaluating function provide a reliable band score for the Lexical Resource criterion.

        After carefully reviewing the essay text {essay}, generate a comprehensive report that lists and categorizes the lexical errors and mistakes found in the essay. Provide specific examples from the essay to support your observations.

        The goal is to produce a consistent and reliable report that can assist the main evaluating function in determining an accurate band score for the essay's Lexical Resource based on the IELTS Writing {task} criteria.

        Report Structure:

        Vocabulary Errors:

        - Identify any errors related to vocabulary usage, such as incorrect word choice, inaccurate meaning, or inappropriate register.
        - Provide a clear count of the total number of vocabulary errors found in the essay.
        - Include specific examples of vocabulary errors from the essay.
        
        Word Formation Errors:

        - Identify any errors related to word formation, such as incorrect prefixes, suffixes, or parts of speech.
        - Provide a clear count of the total number of word formation errors found in the essay.
        - Include specific examples of word formation errors from the essay.
        
        Spelling Errors:

        - Identify any spelling errors in the essay.
        - Provide a clear count of the total number of spelling errors found in the essay.
        - Include specific examples of spelling errors from the essay.
        
        Collocation Errors:

        - Identify any errors related to collocations, such as incorrect word combinations or awkward phrasing.
        - Provide a clear count of the total number of collocation errors found in the essay.
        - Include specific examples of collocation errors from the essay.
        
        Repetition and Redundancy:

        - Identify instances of unnecessary repetition or redundancy in the vocabulary used.
        - Provide a clear count of the total number of repetition and redundancy issues found in the essay.
        - Include specific examples of repetition and redundancy from the essay.
        
        Lexical Range and Sophistication:

        - Assess the range and sophistication of vocabulary used in the essay.
        - Identify any instances of overuse or underuse of certain words or phrases.
        - Provide suggestions for improving lexical diversity and sophistication.
        
        also consider this terms carfully:
        - Using a wide range of vocabulary accurately and appropriately
        - Demonstrating the ability to use less common lexical items
        - Avoiding repetition by using synonyms or paraphrasing
        - Spelling words correctly and this is a brief of the mistakes that writer has done in his essay {grammar_check}
        

        Total Lexical Error Count:

        Provide the total count of all lexical errors and mistakes identified in the essay.
        Lexical Error Severity:

        Suggested Band Score:

        Provide a suggested band score for the essay based on the following criteria:
        If the essay contains significant errors (more than 10) and lacks coherence or task fufilment, suggest a score between 3 and 5, and provide a specific score with justification.
        If the essay is well-written, addresses the task effectively, and contains only minor errors (fewer than 5), suggest a score between 6 and 9, and provide a specific score with justification.
        Support the suggested band score by referencing specific strengths and weaknesses identified in the report, as well as the error count.
        Please provide a detailed and objective analysis of the essay, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations and provide constructive suggestions for improvement in each area. Be precise in your analysis and ensure that all mistakes and areas needing improvement are addressed.

        Assess the severity of the identified lexical errors and their potential impact on the essay's overall quality and comprehensibility.
        Categorize the lexical errors as minor, moderate, or severe based on their frequency and impact on the essay's effectiveness.
        Please provide a detailed and objective analysis of the essay's lexical errors and mistakes, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations.

        To use the generated report in assisting the main evaluating function:

        Carefully review the report, noting the identified lexical errors, their categorization, and the provided examples from the essay.
        Consider the total lexical error count and the severity of the errors in relation to the IELTS Writing {task} Lexical Resource band descriptors.
        Use the insights from the report to guide the evaluation of the essay's performance in the Lexical Resource criterion.
        Ensure consistency in the evaluation by referring to the report's findings and the official IELTS Writing {task} Lexical Resource band descriptors.

"""
lex_prompt = f"""
    You are an IELTS examiner and your role is to assess IELTS Writing Essays. In this task {task}, your focus is to evaluate only the LEXICAL RESOURCE of the given essay {essay} based on the official LEXICAL RESOURCE assessment criteria provided by IELTS.org.
    
     to help you while evaluating i created  analysis tool that can first before your evalation make an intial evalaution of the aimed essay 
        and this will guide you to the most significant mistakes and errors are existed in the essay that might affect the finall score of task response
        and this will give you the confidence that you make an efficiant evalaution 
        
        and you should use this analysis in your assessment and take all the time you need the most important thing is provide a reliable score for the citeria
    important Note:
        in the analysis based on the mistakes are in the essay it will provide a suggetion of the score that might be lower than yours please you should consider that 
        and that might mean that your evaluation was inaccurate and you then will mislead the ielts taker who is rely on you 
        so please make sure you do not be misleader for them and i created this tool because i want you to be the best so please consider this effort
        
        now i will give you the result of the analysis and make as a guide for you trust me it will give you things will diffentely help you
        this is the analysis of the essay {lexic} 
        
        and to make it is to you to decide the deserved score which i am confident you will do that here is the suggested band score that the tool estimated for you because it wants helping you {suggeted_score}
        
        i hope you will not let me down and use what i told you above 

    
    Instructions for assessing LEXICAL RESOURCE:
    LEXICAL RESOURCE (LR) :
    This criterion refers to the range of vocabulary the candidate has used and the 
    accuracy and appropriacy of that use in terms of the specific task. 
    The LR criterion assesses:
    
    - the range of general words used (e.g. the use of synonyms to avoid repetition)
    - the adequacy and appropriacy of the vocabulary (e.g. topic-specific items, 
      indicators of writer’s attitude). 
    - the precision of word choice and expression. 
    - the control and use of collocations, idiomatic expressions and sophisticated 
      phrasing. 
    - the density and communicative effect of errors in spelling. 
    - the density and communicative effect of errors in word formation.
    
    also consider this terms carfully:
    - Using a wide range of vocabulary accurately and appropriately
    - Demonstrating the ability to use less common lexical items
    - Avoiding repetition by using synonyms or paraphrasing
    - Spelling words correctly and this is a brief of the mistakes that writer has done in his essay {grammar_check}
    

    
    Be objective and unbiased in your assessment, ensuring that your evaluation is based solely on the IELTS criteria and not influenced by the essay's topic, stance, or the candidate's language background.
    
    Band descriptors for the LR criterion:
    
    Band 9: Full flexibility and precise use are widely evident. A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features. Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.
        
    Band 8: A wide resource is fluently and flexibly used to convey precise meanings. There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation. Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.
        
    Band 7: The resource is sufficient to allow some flexibility and precision. There is some ability to use less common and/or idiomatic items. An awareness of style and collocation is evident, though inappropriacies occur. There are only a few errors in spelling and/or word formation and they do not detract from overall clarity.
        
    Band 6: The resource is generally adequate and appropriate for the task. The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice. If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy. There are some errors in spelling and/or word formation, but these do not impede communication.
        
    Band 5: The resource is limited but minimally adequate for the task. Simple vocabulary may be used accurately but the range does not permit much variation in expression. There may be frequent lapses in the appropriacy of word choice and a lack of flexibility is apparent in frequent si mplifications and/or repetitions. Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.
        
    Band 4: The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively. There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material). I nappropriate word choice and/or errors in word formation and/or in spelling may impede meaning.
        
    Band 3: The resource is inadequate (which may be due to the response being significantly underlength). Possible over-dependence on input material or memorised language. Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning.
        
    Band 2: The resource is extremely limited with few recognisable strings, apart from memorised phrases. There is no apparent control of word formation and/or spellin
        
    Band 1: Responses of 20 words or fewer are rated at Band 1. No resource is apparent, except for a few isolated words.
        
    Band 0: The candidate did not attempt the task, so no assessment of lexical resource can be made.
    
    
    Structure your response as follows:

Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

Evaluation: To guide your evaluation, follow these steps:
1- Carefully review the essay prompt and the candidate's response.
2- Analyze the range and variety of vocabulary used in the essay. Is there evidence of a broad lexical repertoire?
3- Evaluate the accuracy and appropriateness of the vocabulary used. Are words and phrases employed correctly and effectively to convey meaning?
4- Assess the candidate's ability to use less common lexical items, such as idiomatic expressions, colloquialisms, or subject-specific terminology, where appropriate.
5- Examine the candidate's skill in conveying precise meaning through their choice of words and phrases. Are they able to express ideas clearly and specifically?
6- Determine the band score (1-9) for Lexical Resource based on the official IELTS band descriptors. Provide a brief justification for your score.
7- Identify 2-3 specific strengths of the essay's Lexical Resource, providing examples from the text to support your points.
8- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Lexical Resource.
9- Comment on the candidate's ability to paraphrase the language from the prompt effectively and avoid repetition of words or phrases.
10- Provide an overall assessment of the essay's Lexical Resource, highlighting the main takeaways and offering encouragement for future improvement.

Please note that your evaluation should be unbiased and based solely on the IELTS lexical resource criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.
    
Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS writing {task} skills and achieve their desired band score.
    """
# grammmar and accuracy criteria prompt
gr_prompt = f"""
    You are an IELTS examiner and your role is to assess IELTS Writing Essays. In this task {task}, your focus is to evaluate only the GRAMMATICAL RANGE AND ACCURACY of the given essay {essay} based on the official GRAMMATICAL RANGE AND ACCURACY assessment criteria provided by IELTS.org.

    before starting evalauting take a look to this analysis of task response of the essay and you should cosider the following based on the report or the analysis of the aimed essay:

    1- this is a report writen to help you consider many things that you might neglect or miss while evaluating
    2- you should consider the report in your evalaution but do not rely on it to much make it as a refernce that might help you witie an accurate band score
    3- it will give you the state of the essay or specifically the errors in the essay and you should consider them in your own evalauation
    4- when you write the finall score you should consider that you have considered the report, this report will help you make a reliable score of the criteria
    5- when you write the finall assement do not mention the report
    
    you should consider this grammar analysis {grammar_check} please consider the mistakes int he essay

    Instructions for assessing GRAMMATICAL RANGE AND ACCURACY:
    GRAMMATICAL RANGE AND ACCURACY (GRA):
    This criterion refers to the range and accurate use of the candidate'’'s grammatical 
    resource via the candidate's writing at sentence level. 
    The GRA criterion assesses:
    
    - the range and appropriacy of structures used in a given response (e.g. simple,
      compound and complex sentences).
    - the accuracy of simple, compound and complex sentences.
    - the density and communicative effect of grammatical errors.
    - the accurate and appropriate use of punctuation.
    
    and also you should consider this when evalauting carfully:
        - Employing a variety of complex sentence structures
        - Maintaining control over grammar and punctuation
        - Avoiding errors that impede understanding or communication
        - Demonstrating the ability to use both simple and complex grammatical forms accurately
    

    Be objective and unbiased in your assessment, ensuring that your evaluation is based solely on the IELTS criteria and not influenced by the essay's topic, stance, or the candidate's language background.
    
    Band descriptors for the GRA criterion:
    
    Band 9: A wide range of structures is used with full flexibility and control. Punctuation and grammar are used appropriately throughout. Minor errors are extremely rare and have minimal impact on communication.
    
    Band 8: A wide range of structures is flexibly and accurately used. The majority of sentences are error-free, and punctuation is well managed. Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.
    
    Band 7: A variety of complex structures is used with some flexibility and accuracy. Grammar and punctuation are generally well controlled, and error-free sentences are frequent. A few errors in grammar may persist, but these do not impede communication.
    
    Band 6: A mix of simple and complex sentence forms is used but flexibility is limited. Examples of more complex structures are not marked by the same level of accuracy as in simple structures. Errors in grammar and punctuation occur, but rarely impede communication.
    
    Band 5: The range of structures is limited and rather repetitive. Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences. Grammatical errors may be frequent and cause some difficultyfor the reader. Punctuation may be faulty.
    
    Band 4: A very limited range of structures is used. Subordinate clauses are rare and simple sentences predominate. Some structures are produced accurately but grammatical errors are frequent and may impede meaning. Punctuation is often faulty or inadequate.
    
    Band 3: Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through. Length may be insufficient to provide evidence of control of sentence forms.
    
    Band 2: There is little or no evidence of sentence forms (except in memorised phrases).
    
    Band 1: Responses of 20 words or fewer are rated at Band 1. No rateable language is evident.
    
    Band 0: The candidate did not attempt the task.
   
   
    
    Structure your response as follows:

    Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

    Evaluation: To guide your evaluation, follow these steps:
    1- Carefully review the essay prompt and the candidate's response.
    2- Analyze the range and variety of grammatical structures used in the essay. Is there evidence of a broad grammatical repertoire?
    3- Evaluate the accuracy and appropriateness of the grammatical structures employed. Are sentences constructed correctly and effectively to convey meaning?
    4- Assess the candidate's ability to use complex grammatical structures, such as subordinate clauses, conditional sentences, or passive voice, where appropriate.
    5- Examine the candidate's skill in producing error-free sentences. Are there minimal or no grammatical errors that impede understanding?
    6- Determine the band score (1-9) for Grammatical Range and Accuracy based on the official IELTS band descriptors. Provide a brief justification for your score.
    7- Identify 2-3 specific strengths of the essay's Grammatical Range and Accuracy, providing examples from the text to support your points.
    8- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Grammatical Range and Accuracy.
    9- Comment on the candidate's ability to maintain grammatical control in longer, more complex sentences and avoid errors that impede understanding.
    10- Provide an overall assessment of the essay's Grammatical Range and Accuracy, highlighting the main takeaways and offering encouragement for future improvement.

    Please note that your evaluation should be unbiased and based solely on the IELTS GRAMMATICAL RANGE AND ACCURACY criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.
    
    Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS writing {task} skills and achieve their desired band score.
    """
# task response task 1 acadimic criteria prompt  
tas_academic_task1_analysis = f"""
        You are an IELTS writing assistant tasked with analyzing IELTS Writing Task 1 essays. Your primary focus is to identify potential issues that may impact the Task Response score, based on the official IELTS Task Response criteria for Task 1.

        After carefully reviewing the essay text {essay}, generate a comprehensive report that highlights the identified issues and provides specific examples from the essay to support your observations. Structure the report in a way that aligns with the IELTS Task Response criteria for Task 1.

        The goal is to produce a consistent and reliable report that can guide the evaluation of the essay's Task Response and provide valuable feedback to the candidate.

        Report Structure:

        Overview:

       - Assess if the essay provides a clear overview of the main features or key information from the given data/diagram.
       - Identify any missing or irrelevant information in the overview.
       - Provide concise suggestions for improving the overview.
       
        Key Features:

        - Evaluate if the essay covers the key features or trends presented in the data/diagram.
        - Identify any missing or irrelevant key features.
        - Offer specific recommendations to better highlight and explain the key features.
        
         Data Comparison and Accuracy:

        - Assess if the essay accurately compares and contrasts the relevant data points or information.
        - Identify any inaccuracies, inconsistencies, or misinterpretations of the data.
        - Provide clear guidance for improving data comparison and accuracy.
        
        Logical Structure and Coherence:

        - Evaluate the logical structure and coherence of the essay.
        - Identify any areas where the flow of information is unclear or disjointed.
        - Suggest concrete ways to enhance the logical structure and coherence of the response.
        
       

        
        if the question asks the candidate to describe key features and make comparisons, 
         but the candidate only describes the features without making comparisons, they will lose points in 
         Task Response. Similarly, if the candidate misinterprets the data or describes irrelevant information, 
         their score will be lowered. and the question is {question}

        Word Count:

        Aim to write between 150-180 words and number of words in the essay is {num_words}
        Ensure all key features are covered in sufficient detail if the number of words more than 220 this is a bad thing and would affect the score
        
        
        Error Analysis:

        Carefully review the essay and identify any grammatical, lexical, and cohesive errors.
        Provide a clear count of the total number of errors found in the essay.
        Classify the errors into categories (e.g., grammar, vocabulary, coherence) to help guide feedback.
        
        Suggested Band Score:

        Provide a suggested band score for the essay based on the following criteria:
        If the essay contains significant errors (more than 10) and lacks coherence, suggest a score between 3 and 5, and provide a specific score with justification.
        If the essay is well-written, addresses the task effectively, and contains only minor errors (fewer than 5), suggest a score between 6 and 9, and provide a specific score with justification.
        Support the suggested band score by referencing specific strengths and weaknesses identified in the report, as well as the error count.
        Please provide a detailed and objective analysis of the essay, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations and provide constructive suggestions for improvement in each area. Be precise in your analysis and ensure that all mistakes and areas needing improvement are addressed.

        To use the generated report in evaluating the Task 1 essay:

        Carefully review the report, noting the identified issues, error count, and provided examples from the essay.
        Assess the severity and impact of each identified issue and error on the essay's Task Response.
        Consider the provided suggestions for improvement and determine if the candidate has effectively addressed these aspects in their essay.
        Use the insights from the report, including the error count and suggested band score, to guide your evaluation of the essay's Task Response, in conjunction with the official IELTS Task Response band descriptors for Task 1.
        Ensure consistency in your evaluation by referring to the report's findings and the official band descriptors.
    """    
tas_academic_task1 = f"""
     You are an IELTS examiner and your role is to assess IELTS Writing Essays. In this task {task}, your focus is to evaluate only the Task Response of the given essay {essay} based on the official Task Response assessment criteria provided by IELTS.org.

        to help you while evaluating i created  analysis tool that can first before your evalation make an intial evalaution of the aimed essay 
        and this will guide you to the most significant mistakes and errors are existed in the essay that might affect the finall score of task response
        and this will give you the confidence that you make an efficiant evalaution 
        
        and you should use this analysis in your assessment and take all the time you need the most important thing is provide a reliable score for the citeria
    Note:
        in the analysis based on the mistakes are in the essay it will provide a suggetion of the score that might be lower than yours please you should consider that 
        and that might mean that your evaluation was inaccurate and you then will mislead the ielts taker who is rely on you 
        so please make sure you do not be misleader for them and i created this tool because i want you to be the best so please consider this effort
        
        now i will give you the result of the analysis and make as a guide for you trust me it will give you things will diffentely help you
        this is the analysis of the essay {task_resp_1_aca} also to further helping you this is a grammar chacker that i also created 
        to help you know the most mistakes that the writer made in his eesay and i want you to use it in your evalaution 
        this is the analysis of the grammar {grammar_check}
        
        and to make it is to you to decide the deserved score which i am confident you will do that here is the suggested band score that the tool estimated for you because it wants helping you {suggeted_score}
        
        i hope you will not let me down and use what i told you above 
        
        
     Instructions for assessing Task Response in {task}:
     This Writing {task} has a defined input and a largely predictable output. It is basically an 
     information-transfer task, which relates narrowly to the factual content of a diagram, 
     graph, table, chart, map or other visual input, not to speculative explanations that lie 
     outside the given data. and the here is the description of the chart or whatever the task {describe_image} if it is avaliable and you should use it as a referance
     The TA criterion assesses the ability to summarise the information provided in the 
     diagram by: 
     - selecting key features of the information. 
     - providing sufficient detail to illustrate these features. 
     - reporting the information, figures and trends accurately. 
     - comparing or contrasting the information by adequately highlighting the identifiable trends, principal changes or differences in the data and other inputs (rather than mechanical description reporting detail). 
     - presenting the response in an appropriate format.
    
        
     Be objective and unbiased in your assessment, ensuring that your evaluation is based solely on the IELTS criteria .
    
     band descriptors for the task response task 1 criterion:
    
     Band 9: All the requirements of the task are fully and appropriately satisfied.
    
     Band 8: The response covers all the requirements of the task appropriately, relevantly and sufficiently. 
         There may be occasional omissions or lapses in content. Key features are skilfully selected, and clearly presented, highlighted and illustrated
    
     Band 7: The response covers the requirements of the task. The content is relevant and accurate – 
         there may be a few omissions or lapses. The format is appropriate.  Key features which are selected are covered and clearly highlighted but could be more fully or more appropriately illustrated or extended. 
         It presents a clear overview, the data are appropriately categorised, and main trends or differences are identified.
    
     Band 6: The response focuses on the requirements of the task and an appropriate format is used. Some irrelevant, 
         inappropriate or inaccurate information may occur in areas of detail or when illustrating or extending the main points. 
         Some details may be missing (or excessive) and further extension or illustration may be needed. Key features which are selected are covered and adequately highlighted. A relevant overview is attempted. Information is appropriately 
         selected and supported using figures/data.
    
     Band 5: The response generally addresses the requirements of the task. The format may be inappropriate in places. 
         There may be a tendency to focus on details (without referring to the bigger picture). The inclusion of irrelevant, 
         inappropriate or inaccurate material in key areas detracts from the task achievement. There is limited detail when extending and illustrating the main points. 
         Key features which are selected are not adequately covered. The recounting of detail is mainly mechanical. There may be no data to support the description.
    
     Band 4: The response is an attempt to address the task. Few key features have been selected.  Few key features have been selected.
    
     Band 3: Key features/bullet points which are presented may be irrelevant, repetitive, inaccurate or inappropriate. 
     The response does not address the requirements of the task (possibly because of misunderstanding of the data/diagram/situation). Key features/bullet points which are presented may be largely irrelevant. Limited information is presented, and this may be used repetitively.
    
     Band 2: The content barely relates to the task.
    
     Band 1: The content is wholly unrelated to the task. Any copied rubric must be discounted. Responses of 20 words or fewer are rated at Band 1.
    
    
     Structure your response as follows:
         if the question asks the candidate to describe key features and make comparisons, 
          but the candidate only describes the features without making comparisons, they will lose points in 
          Task Response. Similarly, if the candidate misinterprets the data or describes irrelevant information, 
          their score will be lowered. and the question is {question}
          
     Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

     Evaluation: To guide your evaluation, follow these steps:
     1- Carefully review the task prompt and the candidate's response.
     2- Analyze how accurately and completely the candidate summarizes the information from the graph, table, chart, or diagram. Consider the inclusion of key features and trends.
     3- Evaluate the candidate's ability to make relevant comparisons between data points or visual elements. Are the comparisons meaningful and well-supported?
     4- Assess the clarity and coherence of the response. Is there a logical flow of information, with clear connections between sentences and paragraphs?
     5- Determine the band score (1-9) for Task Response based on the official IELTS band descriptors. Provide a brief justification for your score.
     6- Identify 2-3 specific strengths of the response's Task Response, providing examples from the text to support your points.
     7- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Task Response.
     8- Comment on the response's adherence to the minimum word count (150 words) and how it impacts the Task Response. If the response is under the word count, suggest ways to expand the content.
     9- Provide an overall assessment of the response's Task Response, highlighting the main takeaways and offering encouragement for future improvement.

     Please note that your evaluation should be unbiased and based solely on the IELTS Task Response criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.

 Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS Academic Writing Task 1 skills and achieve their desired band score."""
# task response task 1 general criteria prompt 
tas_general_task1_analysis = f"""

    You are an IELTS writing assistant tasked with analyzing IELTS Writing Task 1 General essays. Your primary focus is to identify potential issues that may impact the Task Response score, based on the official IELTS Task Response criteria for Task 1 General.

        After carefully reviewing the essay text {essay}, generate a comprehensive report that highlights the identified issues and provides specific examples from the essay to support your observations. Structure the report in a way that aligns with the IELTS Task Response criteria for Task 1 General.

        The goal is to produce a consistent and reliable report that can guide the evaluation of the essay's Task Response and provide valuable feedback to the candidate.

        Report Structure:

        Task Fulfillment:

        - Assess if the essay effectively addresses all parts of the task and provides an appropriate amount of detail.
        - Identify any missing or irrelevant information in the response.
        - Provide concise suggestions for improving task fulfillment.
        
        Tone and Purpose:

        - Evaluate if the essay uses an appropriate tone and register for the given context and purpose.
        - Identify any instances where the tone or register is inconsistent or inappropriate.
        - Offer specific recommendations to better align the tone and register with the task.
        
        Coherence and Cohesion:

        - Assess if the essay is well-organized, with clear progression and logical connections between ideas.
        - Identify any areas where coherence or cohesion is lacking.
        - Provide clear guidance for improving the essay's structure and flow.
        
        Lexical Resource:

        - Evaluate the range and accuracy of vocabulary used in the essay.
        - Identify any errors in word choice, spelling, or word formation.
        - Suggest ways to enhance the lexical resource and avoid repetition.
        
        Grammatical Range and Accuracy:

        - Assess the variety and precision of grammatical structures used in the essay.
        - Identify any grammatical errors or inconsistencies.
        - Provide recommendations for improving grammatical range and accuracy.
        
        you must also consider these terms carfully in evalauting duble check:
        Addressing all parts of the task adequately:

            Identify the purpose of the letter (e.g., request, complaint, invitation)
            Address all bullet points or questions provided in the task
            Include any additional information relevant to the situation
            
        Presenting a clear position:

            Begin with an appropriate salutation and brief introduction
            Clearly state the purpose of the letter in the opening paragraph
            
        Supporting ideas with relevant explanations and examples:

            Provide specific details, explanations, or examples for each bullet point or question
            Use a friendly, polite, or formal tone as appropriate for the situation
            
        Fully developing the topic within the given word count:

            Aim to write between 150-180 words and number of words in the essay is {num_words}
            Ensure all bullet points or questions are addressed in sufficient detail
            Conclude the letter with a suitable closing remark and sign-off
        
        Word Count:

        Check if the essay meets the minimum word count requirement (150 words) and report the actual number of words {num_words}.
        Error Analysis:

        Carefully review the essay and identify any errors related to task fulfillment, coherence, lexical resource, and grammar.
        Provide a clear count of the total number of errors found in the essay.
        Classify the errors into categories (e.g., task fulfillment, coherence, vocabulary, grammar) to help guide feedback.
        Suggested Band Score:

        Provide a suggested band score for the essay based on the following criteria:
        If the essay contains significant errors (more than 10) and lacks coherence or task fulfillment, suggest a score between 3 and 5, and provide a specific score with justification.
        If the essay is well-written, addresses the task effectively, and contains only minor errors (fewer than 5), suggest a score between 6 and 9, and provide a specific score with justification.
        Support the suggested band score by referencing specific strengths and weaknesses identified in the report, as well as the error count.
        Please provide a detailed and objective analysis of the essay, focusing on the aspects mentioned above. Use specific examples from the essay to support your observations and provide constructive suggestions for improvement in each area. Be precise in your analysis and ensure that all mistakes and areas needing improvement are addressed.

        To use the generated report in evaluating the Task 1 General essay:

        1- Carefully review the report, noting the identified issues, error count, and provided examples from the essay.
        2- Assess the severity and impact of each identified issue and error on the essay's Task Response.
        3- Consider the provided suggestions for improvement and determine if the candidate has effectively addressed these aspects in their essay.
        4- Use the insights from the report, including the error count and suggested band score, to guide your evaluation of the essay's Task Response, in conjunction with the official IELTS Task Response band descriptors for Task 1 General.
        5- Ensure consistency in your evaluation by referring to the report's findings and the official band descriptors.


"""       
tas_general_task1 = f"""
you are an IELTS examiner and your roll is to check IELTS Writing Essays in General {task}, your task is to check only the TASK RESPONSE in this {essay} based on the TASK RESPONSE official asssement provided by IELTS.org
  to help you while evaluating i created  analysis tool that can first before your evalation make an intial evalaution of the aimed essay 
        and this will guide you to the most significant mistakes and errors are existed in the essay that might affect the finall score of task response
        and this will give you the confidence that you make an efficiant evalaution 
        
        and you should use this analysis in your assessment and take all the time you need the most important thing is provide a reliable score for the citeria
    important Note:
        in the analysis based on the mistakes are in the essay it will provide a suggetion of the score that might be lower than yours please you should consider that 
        and that might mean that your evaluation was inaccurate and you then will mislead the ielts taker who is rely on you 
        so please make sure you do not be misleader for them and i created this tool because i want you to be the best so please consider this effort
        
        now i will give you the result of the analysis and make as a guide for you trust me it will give you things will diffentely help you
        this is the analysis of the essay {task_resp_1_gen} also to further helping you this is a grammar chacker that i also created 
        to help you know the most mistakes that the writer made in his eesay and i want you to use it in your evalaution 
        this is the analysis of the grammar {grammar_check}
        
        and to make it is to you to decide the deserved score which i am confident you will do that here is the suggested band score that the tool estimated for you because it wants helping you {suggeted_score}
        
        i hope you will not let me down and use what i told you above 
    
This Writing {task} also has a largely predictable output in that each task sets out the 
    context and purpose of the letter and the functions the candidate should cover in 
    order to achieve this purpose. 
    The TA criterion assesses the ability to: 
    - clearly explain the purpose of the letter. 
    - fully address the three bullet-pointed requirements set out in the task. 
    - extend these three functions appropriately and relevantly. 
    - use an appropriate format for the letter. 
    - consistently use a tone appropriate to the task.

    you must also consider these terms carfully in evalauting duble check:
        Addressing all parts of the task adequately:

            Identify the purpose of the letter (e.g., request, complaint, invitation)
            Address all bullet points or questions provided in the task
            Include any additional information relevant to the situation
            
        Presenting a clear position:

            Begin with an appropriate salutation and brief introduction
            Clearly state the purpose of the letter in the opening paragraph
            
        Supporting ideas with relevant explanations and examples:

            Provide specific details, explanations, or examples for each bullet point or question
            Use a friendly, polite, or formal tone as appropriate for the situation
            
        Fully developing the topic within the given word count:

             Aim to write between 150-180 words and number of words in the essay is {num_words}
            Ensure all bullet points or questions are addressed in sufficient detail
            Conclude the letter with a suitable closing remark and sign-off
            
        
you should be fair when you assess this criteria and give a precise band score and provide some explanation 
    important NOTE: when you give the band score it should be a whole number not a decimal number between 0 to 9 and when you give a decimal number round it  
    
    Below are the band descriptors for the task response task 1 criterion:
    
    Band 9: All the requirements of the task are fully and appropriately satisfied.
    
    Band 8: The response covers all the requirements of the task appropriately, relevantly and sufficiently. 
        There may be occasional omissions or lapses in content. All bullet points are clearly presented, 
        and appropriately illustrated or extended.
    
    Band 7: The response covers the requirements of the task. The content is relevant and accurate – 
        there may be a few omissions or lapses. The format is appropriate.  All bullet points are covered and 
        clearly highlighted but could be more fully or more appropriately illustrated or extended. It presents a clear purpose. 
        The tone is consistent and appropriate to the task. Any lapses are minimal.
    
    Band 6: The response focuses on the requirements of the task and an appropriate format is used. Some irrelevant, 
        inappropriate or inaccurate information may occur in areas of detail or when illustrating or extending the main points.
        Some details may be missing (or excessive) and further extension or illustration may be needed. 
        All bullet points are covered and adequately highlighted. The purpose is generally clear. There may be minor inconsistencies in tone.
    
    Band 5: The response generally addresses the requirements of the task. The format may be inappropriate in places. 
        There may be a tendency to focus on details (without referring to the bigger picture. The inclusion of irrelevant, 
        inappropriate or inaccurate material in key areas detracts from the task achievement. 
        There is limited detail when extending and illustrating the main points. All bullet points are presented but one or more may not be adequately covered. 
        The purpose may be unclear at times. The tone may be variable and sometimes inappropriate
    
    Band 4: The response is an attempt to address the task. he format may be inappropriate. Few key features have been selected.  Not all bullet points are presented.  
        The purpose of the letter is not clearly explained and may be confused. The tone may be inappropriate
    
    Band 3: Key features/bullet points which are presented may be irrelevant, repetitive, inaccurate or inappropriate. The response does not address the requirements of the task (possibly because of misunderstanding of the data/diagram/situation). Key features/bullet points which are presented may be largely irrelevant. Limited information is presented, and this may be used repetitively.
    
    Band 2: The content barely relates to the task.
    
    Band 1: The content is wholly unrelated to the task. Any copied rubric must be discounted. Responses of 20 words or fewer are rated at Band 1.
    
    
    Structure your response as follows:

    Band Score: Provide a whole number score between 0 and 9. If your initial assessment yields a decimal score, round it to the nearest whole number.

    Evaluation: To guide your evaluation, follow these steps:
    1- Carefully review the essay prompt and the candidate's response.
    2- Analyze how well the candidate fulfills the purpose of the task, such as making a request, giving information, or explaining a situation. Consider the clarity and effectiveness of the message.
    3- Evaluate the candidate's coverage of all required points mentioned in the prompt. Are all key points addressed adequately?
    4- Assess the appropriateness of the tone and style of the response for the given context and recipient. Is the language formal or informal, polite or friendly, as required by the situation?
    5- Determine the band score (1-9) for Task Response based on the official IELTS band descriptors. Provide a brief justification for your score.
    6- Identify 2-3 specific strengths of the response's Task Response, providing examples from the text to support your points.
    7- Suggest 2-3 areas for improvement, offering concrete examples and actionable advice on how to enhance the Task Response.
    8- Comment on the response's adherence to the minimum word count (150 words) and how it impacts the Task Response. If the response is under the word count, suggest ways to expand the content.
    9- Provide an overall assessment of the response's Task Response, highlighting the main takeaways and offering encouragement for future improvement.

    Please note that your evaluation should be unbiased and based solely on the IELTS Task Response criteria. Assess the essay fairly and objectively, regardless of its topic or the candidate's personal background.

    Remember to maintain a supportive and constructive tone throughout your evaluation. Your goal is to provide valuable insights and practical suggestions that can help the candidate refine their IELTS General Training Writing Task 1 skills and achieve their desired band score.
"""





task1_band_score = []
task2_band_score = []
def remove_band_score(result):
    num = float(extract_digit_from_essay(result))
    if '**Band Score**:' in result:
        # print('True')
        pattern = re.compile(r'\*{0,2}Band Score\*{0,2}:?\s*\*{0,2}\d+(\.\d+)?\*{0,2}\n?|\*+\n?', re.IGNORECASE)
    else:
        # print('False')
        pattern = re.compile(r'(\*{2})?Band Score:?(\*{2})?\s*\d+(\.\d+)?(\*{2})?\n+', re.IGNORECASE)
    cleaned_result = pattern.sub('', result)
    print(num)
    st.markdown(f"**Score: {round(num - 0.1)}**")
    if task == 'Task 1':
        
        task1_band_score.append((round(num - 0.1)))
    else:
        task2_band_score.append((round(num - 0.1)))
    st.write(cleaned_result)
    # print(cleaned_result)
    # print('---------')



task_response = f""""""
if task == 'Task 1' and gen_acad == 'Academic':
    task_response = tas_academic_task1
elif task == 'Task 1' and gen_acad == 'General':
    task_response = tas_general_task1

else:
    task_response = tas_prompt

def extract_digit_from_essay(essay):
    digit = re.search(r'(?:^|\D)([3-9](?:\.\d+)?)(?!\d)', essay)
    if digit:
        return digit.group(1)
    else:
        return None
 
def delay(num_sec=5):
    delay_seconds = num_sec  # Adjust the delay as needed
    print(f"Waiting for {delay_seconds} seconds before evaluating...")
    time.sleep(delay_seconds)


def evaluate2(prompt):
    genai.configure(api_key = used_key)
    max_retries = number_of_tries
    retries = 0
    while retries < max_retries:
        try:
            task = model.generate_content(prompt, stream=True)
            task.resolve()
            task_ch = task.text
            remove_band_score(task_ch)
            break  # Break out of the while loop if the generation is successful
        except Exception  as e:
            retries += 1
            print("An internal error has occurred: now will use ", e)
            print("Retrying...")
            continue
    else:
        claude_model(haiku, prompt)



# if button:
#     if email is not None and email.strip() != "":
#         with open('registered_emails.csv', 'r') as file:
#                 reader = csv.reader(file)
#                 emails = [row[0] for row in reader]
#                 if email in emails:
#                     if q_words == 0:
#                         st.error(f'Please write the question ')
#                     elif num_words == 0:
#                         st.error(f'Please write your essay')
#                     elif task == 'Task 1' and num_words < 150 :
#                         st.error(f'Your essay is short the written words is {num_words}, please continue writing, it should be at least 150 words')
#                     elif task == 'Task 2' and num_words < 250:
#                         st.error(f'Your essay is short the written words is {num_words}, please continue writing, it should be at least 250 words')
#                     else:
                        
#                         st.markdown('---')
#                         # decripe_image(used_key)
                        
#                         st.markdown("## Task Response")
#                         try:
#                             grammar_checker = grammar_spelling2()
#                             grammar_check += grammar_checker
#                         except Exception  as e:
#                             print("An internal error has occurred: now will use ", e)
                            
                            
#                         if task == 'Task 1':
#                             if gen_acad == 'Academic':
                                
#                                 if chart_image is not None:
#                                     described_image = decripe_image(used_key, image_pil)
#                                     describe_image += described_image
#                                     # print(describe_image)
#                                 TR_task1_aca = essay_analysis(tas_academic_task1_analysis)
#                                 task_resp_1_aca += TR_task1_aca
#                                 suggest = suggested_score_ana(task_resp_1_aca, task)  
#                                 suggeted_score += suggest
#                                 print(suggest)
                                
#                             else:
#                                 TR_task1_gen = essay_analysis(tas_general_task1_analysis)
#                                 task_resp_1_gen += TR_task1_gen
#                                 suggest = suggested_score_ana(task_resp_1_gen, task)  
#                                 suggeted_score += suggest
                        
#                         if task == 'Task 2':
#                             TR_task2 = essay_analysis(tr_task2_analysis)
#                             TR_task += TR_task2
#                             suggest = suggested_score_ana(TR_task, task)  
#                             suggeted_score += suggest
#                         delay(10)
#                         evaluate2(task_response)
                        
#                         suggeted_score = ''
#                         print('suggested score 1:', suggeted_score)
                        
#                         st.markdown('---')
#                         st.markdown("## Coherence and Cohesion")
#                         CO_task2 = essay_analysis(co_task2_analysis)
#                         coherence += CO_task2
#                         suggest = suggested_score_ana(CO_task2, task)  
#                         suggeted_score += suggest
#                         # delay(10)
#                         evaluate2(co_prompt)
#                         suggeted_score = ''
#                         print('suggested score 2:', suggeted_score)
#                         st.markdown('---')
#                         st.markdown("## Lexical Resources")
#                         LX_task2 = essay_analysis(lex_task2_analysis)
#                         lexic += LX_task2 
#                         suggest = suggested_score_ana(LX_task2, task)  
#                         suggeted_score += suggest  
#                         # delay(11)
#                         evaluate2(lex_prompt)
#                         suggeted_score = ''
#                         print('suggested score 3:', suggeted_score)
#                         st.markdown('---')
#                         st.markdown("## Grammar and Acurracy")
#                         evaluate2(gr_prompt)
#                         suggeted_score = ''
#                         st.markdown('**- Grammar and Spelling mistakes**')
#                         grammar_spelling()
                        
#                         st.markdown('---')
                        
#                         if task == 'Task 1':
#                             overall_score = round(sum(task1_band_score) /4)
#                         else:
#                             overall_score = round(sum(task2_band_score) /4)
#                         st.markdown(f"## {task} Band Score: {float(overall_score)} / 9")
#                         st.markdown('---')
#                         st.markdown('## Here is the most repeated words in your essay')
#                         stop_w = set(STOPWORDS)
                            
#                         word_cloud = WordCloud(stopwords=stop_w, width= 800, height=400, background_color='white').generate(essay)
#                         img = word_cloud.to_image()
#                         st.image(img)
#                         st.markdown('---')
#                         words_charts()
#                         st.markdown('---')
#                         st.markdown('### Recommended Synonyms of the repeated words')
#                         synonym(Gemini_API_Key2)
#                         st.markdown('---')
                        
#                         st.markdown('### a rewritten version of your essay')
#                         rewrite_essay(Gemini_API_Key3)
#                 else:
#                     st.error("Your email is not rigestered, please rigester your email and try again")
            
#     #         # print((task1_band_score))
#     #         # print((task2_band_score))
#     else:
#         st.error("PLease rigester your email")   


if button:
    
                    if q_words == 0:
                        st.error(f'Please write the question ')
                    elif num_words == 0:
                        st.error(f'Please write your essay')
                    elif task == 'Task 1' and num_words < 150 :
                        st.error(f'Your essay is short the written words is {num_words}, please continue writing, it should be at least 150 words')
                    elif task == 'Task 2' and num_words < 250:
                        st.error(f'Your essay is short the written words is {num_words}, please continue writing, it should be at least 250 words')
                    else:
                        
                        st.markdown('---')
                        # decripe_image(used_key)
                        st.write("Please wait a few seconds until the evaluation appears")
                        st.markdown("## Task Response")
                        try:
                            grammar_checker = grammar_spelling2()
                            grammar_check += grammar_checker
                        except Exception  as e:
                            print("An internal error has occurred: now will use ", e)
                            
                            
                        if task == 'Task 1':
                            if gen_acad == 'Academic':
                                
                                if chart_image is not None:
                                    described_image = decripe_image(used_key, image_pil)
                                    describe_image += described_image
                                    # print(describe_image)
                                TR_task1_aca = essay_analysis(tas_academic_task1_analysis)
                                task_resp_1_aca += TR_task1_aca
                                suggest = suggested_score_ana(task_resp_1_aca, task)  
                                suggeted_score += suggest
                                print(suggest)
                                
                            else:
                                TR_task1_gen = essay_analysis(tas_general_task1_analysis)
                                task_resp_1_gen += TR_task1_gen
                                suggest = suggested_score_ana(task_resp_1_gen, task)  
                                suggeted_score += suggest
                        
                        if task == 'Task 2':
                            TR_task2 = essay_analysis(tr_task2_analysis)
                            TR_task += TR_task2
                            suggest = suggested_score_ana(TR_task, task)  
                            suggeted_score += suggest
                        delay(10)
                        evaluate2(task_response)
                        
                        suggeted_score = ''
                        print('suggested score 1:', suggeted_score)
                        
                        st.markdown('---')
                        st.markdown("## Coherence and Cohesion")
                        CO_task2 = essay_analysis(co_task2_analysis)
                        coherence += CO_task2
                        suggest = suggested_score_ana(CO_task2, task)  
                        suggeted_score += suggest
                        # delay(10)
                        evaluate2(co_prompt)
                        suggeted_score = ''
                        print('suggested score 2:', suggeted_score)
                        st.markdown('---')
                        st.markdown("## Lexical Resources")
                        LX_task2 = essay_analysis(lex_task2_analysis)
                        lexic += LX_task2 
                        suggest = suggested_score_ana(LX_task2, task)  
                        suggeted_score += suggest  
                        # delay(11)
                        evaluate2(lex_prompt)
                        suggeted_score = ''
                        print('suggested score 3:', suggeted_score)
                        st.markdown('---')
                        st.markdown("## Grammar and Acurracy")
                        evaluate2(gr_prompt)
                        suggeted_score = ''
                        st.markdown('**- Grammar and Spelling mistakes**')
                        grammar_spelling()
                        
                        st.markdown('---')
                        
                        if task == 'Task 1':
                            overall_score = round(sum(task1_band_score) /4)
                        else:
                            overall_score = round(sum(task2_band_score) /4)
                        st.markdown(f"## {task} Band Score: {float(overall_score)} / 9")
                        st.markdown('---')
                        st.markdown('## Here is the most repeated words in your essay')
                        stop_w = set(STOPWORDS)
                            
                        word_cloud = WordCloud(stopwords=stop_w, width= 800, height=400, background_color='white').generate(essay)
                        img = word_cloud.to_image()
                        st.image(img)
                        st.markdown('---')
                        words_charts()
                        st.markdown('---')
                        st.markdown('### Recommended Synonyms of the repeated words')
                        synonym(Gemini_API_Key2)
                        st.markdown('---')
                        
                        st.markdown('### a rewritten version of your essay')
                        rewrite_essay(Gemini_API_Key3)
               

# if button:
    
#                         st.markdown('---')
#                         # decripe_image(used_key)
                        
#                         st.markdown("## Task Response")
#                         grammar_checker = grammar_spelling2()
#                         grammar_check += grammar_checker
#                         if task == 'Task 1':
#                             if gen_acad == 'Academic':
                                
#                                 if chart_image is not None:
#                                     described_image = decripe_image(used_key, image_pil)
#                                     describe_image += described_image
#                                     print(describe_image)
#                                 TR_task1_aca = essay_analysis(tas_academic_task1_analysis)        
#                                 task_resp_1_aca += TR_task1_aca
#                             else:
#                                 TR_task1_gen = essay_analysis(tas_general_task1_analysis)
#                                 task_resp_1_gen += TR_task1_gen
                        
#                         if task == 'Task 2':
#                             TR_task2 = essay_analysis(tr_task2_analysis)
#                             TR_task += TR_task2
                        
#                         evaluate2(task_response)
                        
#                         st.markdown('---')
#                         st.markdown("## Coherence and Cohesion")
#                         CO_task2 = essay_analysis(co_task2_analysis)
#                         coherence += CO_task2
#                         evaluate2(co_prompt)
#                         st.markdown('---')
#                         st.markdown("## Lexical Resources")
#                         LX_task2 = essay_analysis(lex_task2_analysis)
#                         lexic += LX_task2   
#                         evaluate2(lex_prompt)
#                         st.markdown('---')
#                         st.markdown("## Grammar and Acurracy")
#                         evaluate2(gr_prompt)
#                         st.markdown('**- Grammar and Spelling mistakes**')
#                         grammar_spelling()
                        
#                         st.markdown('---')
                        
#                         if task == 'Task 1':
#                             overall_score = round(sum(task1_band_score) /4)
#                         else:
#                             overall_score = round(sum(task2_band_score) /4)
#                         st.markdown(f"## {task} Band Score: {float(overall_score)} / 9")
#                         st.markdown('---')
#                         st.markdown('## Here is the most repeated words in your essay')
#                         stop_w = set(STOPWORDS)
                            
#                         word_cloud = WordCloud(stopwords=stop_w, width= 800, height=400, background_color='white').generate(essay)
#                         img = word_cloud.to_image()
#                         st.image(img)
#                         st.markdown('---')
#                         words_charts()
#                         st.markdown('---')
#                         st.markdown('### Recommended Synonyms of the repeated words')
#                         synonym(Gemini_API_Key2)
#                         st.markdown('---')
                        
#                         st.markdown('### a rewritten version of your essay')
#                         rewrite_essay(Gemini_API_Key3)
     
