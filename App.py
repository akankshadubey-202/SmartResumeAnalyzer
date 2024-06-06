import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')
import streamlit as st
import nltk
import spacy
import sqlite3  # Import SQLite3
from sqlite3 import Error
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random
from streamlit_tags import st_tags
from PIL import Image
import datetime
import time
import base64
import pandas as pd
import pafy
import plotly.express as px
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos, job_recommendations
from pytube import YouTube
import streamlit as st

ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                              'streamlit']
web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']

def job_recommender(job_list):
    st.subheader("**Job Recommendations🎯**")
    random.shuffle(job_list)
    no_of_jobs = st.slider('Choose Number of Job Recommendations:', 1, 5, 3)
    for i in range(no_of_jobs):
        st.markdown(f"({i+1}) [{job_list[i][0]}]({job_list[i][1]})")

def fetch_yt_video(link):
    try:
        video = YouTube(link)
        return video.title
    except Exception as e:
        print(f"Error fetching YouTube video title: {e}")
        return None
    
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="wide"

)

def run():
    save_image_path = None  # Initialize save_image_path
    with st.container():
        st.title("CareerCraft AI")
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            #show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

    with st.container():
        st.title("What does your Resume have to Say about you?")
        left_column,right_column,third_col=st.columns([0.35,0.3,0.3])
        with left_column:
            if save_image_path:  # Check if save_image_path is not None
                show_pdf(save_image_path)
        with right_column:       
            st.title("**Skills Section**")
                ## Skill shows
            with st.container():
                l_col1,l_col2=st.columns(2)
                with  l_col1:
                    keywords = st_tags(label='### Skills that you have',text='See our skills recommendation',
                                   value=resume_data['skills'], key='1')
                    job_recommender(job_recommendations['Data Science'])
                with l_col2:
                    recommended_skills = []
                    reco_field = ''
                    rec_course = ''
                    for i in resume_data['skills']:
                        if i.lower() in ds_keyword:
                            print(i.lower())
                            reco_field = 'Data Science'
                            recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                              'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                              'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                              'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                              'Streamlit']
                            recommended_keywords = st_tags(label='### Recommended skills.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='ds_recommendation')
                            rec_course = course_recommender(ds_course)
                            break
                        elif i.lower() in ds_keyword:
                            print(i.lower())
                            reco_field = 'Web Development'
                            recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                              'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                            recommended_keywords = st_tags(label='### Recommended skills.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='web_recommendation')
                            break
                            
                        elif i.lower() in android_keyword:
                            print(i.lower())
                            reco_field = 'Android Development'
                            recommended_skills = ['Android', 'Flutter', 'Kotlin', 'XML', 'SDK', 'API Integration']
                            recommended_keywords = st_tags(label='### Recommended Skills.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='android_recommendation')
                            break
                            ## IOS development recommendation
                        elif i.lower() in ios_keyword:
                            print(i.lower())
                            reco_field = 'IOS Development'
                            recommended_skills = ['IOS', 'Swift', 'Xcode', 'SDK', 'API Integration']
                            recommended_keywords = st_tags(label='### Recommended Skills.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='ios_recommendation')     
                            break  
            with st.container():
                if reco_field=='Data Science':
                    st.success("** Our analysis says you are looking for Data Science Jobs **")
                elif reco_field=='Web Development':
                    st.success("** Our analysis says you are looking for Web Development Jobs**")
                elif reco_field=='Android Development':
                    st.success("** Our analysis says you are looking for Android Development Jobs**")
                elif reco_field=='IOS Development':
                    st.success("** Our analysis says you are looking for ISO Development Jobs**")
                
        with third_col:
            ## Courses and Certification recommendation
                
                               ### Resume writing recommendation
                st.title("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Work Experience</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Projects✍</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Technical Skills ⚽</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                        unsafe_allow_html=True)

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                        unsafe_allow_html=True)

                

                st.title("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                
                with st.container():
                    l1,l2=st.columns(2)
                    with l1:
                        st.header("**Resume Writing Tips**")
                        resume_vid = random.choice(resume_videos)
                        res_vid_title =fetch_yt_video(resume_vid)
                        st.video(resume_vid)
                    with l2:
                        st.header("**Interview 👨‍💼 Tips**")
                        interview_vid = random.choice(interview_videos)
                        int_vid_title = fetch_yt_video(interview_vid)
                        st.video(interview_vid)


                
               
run()
