from eval import get_metrics_df
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import pyrebase
from streamlit_tags import st_tags
from email_validator import validate_email, EmailSyntaxError

# configuration key
firebaseConfig = {
  'apiKey': "AIzaSyAX_-ivrVfKeBb8ZS1XyNUpKGqX2wTx0tU",
  'authDomain': "credit-card-fraud-detect-92fbe.firebaseapp.com",
  'projectId': "credit-card-fraud-detect-92fbe",
  'databaseURL': "https://credit-card-fraud-detect-92fbe-default-rtdb.firebaseio.com/",
  'storageBucket': "credit-card-fraud-detect-92fbe.firebasestorage.app",
  'messagingSenderId': "1016300712784",
  'appId': "1:1016300712784:web:40fd437aed850a206bf255",
  'measurementId': "G-XF44GC5BC9"
}

# firebase authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# database
db = firebase.database()

def validate_email(email_address):
    try:
        email = validate_email(email_address)
        return True, None
    except EmailSyntaxError:
        return False, "Invalid email format."    
    except Exception as e:
        return False, f"An error occurred: {e}"
try:
    # check if the key exists in session state
  if 'keep_graphics' not in st.session_state:
      st.session_state.keep_graphics = False
except AttributeError:
    # otherwise set it to false
    st.session_state.keep_graphics = False
    
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = 'A'

if 'tier_option' not in st.session_state:
    st.session_state.tier_option = 'S'
    
if 'tier_option_active' not in st.session_state:
    st.session_state.tier_option_active = 'N'
    
st.markdown("""
<style>
.big-font {
    font-size:21px !important;    
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<h4 class="big-font">Credit Card Fraud Detector Profile </h>', unsafe_allow_html=True)

# authentication
choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type="password")
#if st.session_state.selected_option == "A":
  #  st.header("Detecting Your Transactions with :blue[Advanced Fraud Detection] :male-detective:", divider='gray')
   # st.markdown("""
   # <style>
    #.big-font {
    #    font-size:18px !important;
   # }
  ##  """, unsafe_allow_html=True)
  #  st.markdown('<p class="big-font">Learn from new data and AI-powered analytics to safeguard your financial operations.</p>', unsafe_allow_html=True)
   # st.markdown('<h2 class="big-font">Main Features </h>', unsafe_allow_html=True)
   # st.markdown('<h2 class="big-font">Intelligent Protection: </h>', unsafe_allow_html=True)
  #  st.markdown('<p class="big-font">Our system employs cutting-edge machine learning algorithms to identify suspicious patterns and anomalies in transaction data, before it impacts your business. </p>', unsafe_allow_html=True)
  #  st.markdown('<h2 class="big-font">Comprehensive Dashboard: </h>', unsafe_allow_html=True)
  #  st.markdown('<p class="big-font">Monitor transaction patterns, fraud attempts, and security metrics through an intuitive visual interface designed for both technical and non-technical users. </p>', unsafe_allow_html=True)
  
if choice == 'Sign up': 
    st.session_state.selected_option = 'B'
    st.session_state.hide = False
    st.session_state.keep_graphics = False
    #st.session_state.tier_option_active = False
    re_password = st.sidebar.text_input('Please re-enter your password', type="password")
    handle = st.sidebar.text_input('Please enter your full name', value='')
    # tier selection
    tier = st.sidebar.selectbox('Tier Subscription', ['','Enterprise Tier', 'Mid-Market Tier', 'Growth Tier'])
    
    if tier == 'Enterprise Tier':
        st.cache_resource.clear()
        st.session_state.tier_option = 'A'
        st.session_state.tier_option_active = 'Y'
        if st.session_state.tier_option == "A":
            st.header(':briefcase: Enterprise Tier (Big 5 Banks) Subscription Model', divider='gray')
            st.markdown(':white_check_mark: Monthly base fee: R850,000 to R1,200,000.')
            st.markdown(':white_check_mark: Monthly volume of transactions: up to 15 million.')
            st.markdown(':white_check_mark: Features: include a specialized support staff, unique models, and the entire ML suite.')
            st.markdown(':white_check_mark: One-time implementation fee: R1,800,000–2,500,000.')
    elif tier == 'Mid-Market Tier' :
        st.session_state.tier_option = 'B'
        if st.session_state.tier_option == "B":
            st.header(':briefcase: Mid-Market Tier (Regional Banks and Digital Banks) Subscription Model', divider='gray')
            st.markdown(':white_check_mark: Monthly base fee: R300,000 to R550,000.')
            st.markdown(':white_check_mark: Volume of transactions: up to 3 million per month.')
            st.markdown(':white_check_mark: Features: include priority support and standard ML models.')
            st.markdown(':white_check_mark: One-time implementation fee: R800,000–1,200,000.')
    elif tier == 'Growth Tier':
        st.session_state.tier_option = 'C'
        if st.session_state.tier_option == "C":
            #st.header(":blue[Create Your Secure Account] :closed_lock_with_key:", divider='gray')
            st.header(':briefcase: Growth Tier (Fintechs and Payment Providers) Subscription Model', divider='gray')
            st.markdown(':white_check_mark: Monthly base fee: R80,000 to R200,000.')
            st.markdown(':white_check_mark: Volume of transactions: up to 750,000 per month.')
            st.markdown(':white_check_mark: Features: include standard support and core detecting capabilities.')
            st.markdown(':white_check_mark: One-time implementation fee: R250,000–R450,000.')
    
    submit = st.sidebar.button('Create my account')
    
    if submit:
        #valid, message = validate_email(email)
        #if valid == None:
           # st.error(message)
        #else:
            #st.error(message)
            
        if len(email) == 0:
            st.error("Email Address is required field.")
            st.stop()
        elif len(password) == 0:
            st.error("Password is required field.")
            st.stop()
        elif len(password) < 6:
            st.error("Password must 6 or more characters.")
            st.stop()
        elif len(re_password) == 0:
            st.error("Password confirmation is required field.")
            st.stop()
        elif len(re_password) < 6:
            st.error("Password confirmation must 6 or more characters.")
            st.stop()
        elif password != re_password:
            st.error("Password and Re-Entered Password do not match.")
            st.stop()
        elif len(handle) == 0:
            st.error("Full Name is required field.")
            st.stop()
        elif len(tier) == 0:
            st.error("Please select Tier Subscription.")
            st.stop()
        else:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Account is created successfully!') 
                # sign in
                user = auth.sign_in_with_email_and_password(email, password)
                db.child(user['localId']).child("Fullname").set(handle)
                db.child(user['localId']).child("Tier Subscription").set(tier)
                db.child(user['localId']).child("ID").set(user['localId'])
                st.header('Welcome ' + handle)
                st.info('Access Credit Card Fraud Detection Datshboard via Login/Signup drop down selection by selecting Login option')
            except:
                 st.error('Account already exists!')
    if choice == 'Sign up' and st.session_state.selected_option == 'B' and st.session_state.tier_option_active == 'N':
        st.header(":blue[Create Your Secure Account] :closed_lock_with_key:", divider='gray')
        st.markdown("""
        <style>
        .big-font {
            font-size:18px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<p class="big-font">Join thousands of businesses protecting their financial transactions with our advanced fraud detection platform. Setup takes just minutes, and you will gain immediate access to our comprehensive fraud detection tools.</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="big-font">Form Fields </h>', unsafe_allow_html=True)
        st.markdown(":email: Email Address")
        st.markdown(":lock: Password")
        st.markdown(":writing_hand: Fullname")
        st.markdown(":briefcase: Tier Subscription")
        st.markdown('<h2 class="big-font">Compliance Text </h>', unsafe_allow_html=True)
        st.markdown('<p class="big-font">By creating an account, you agree to our Terms of Service and Privacy Policy. Our platform is full compliant with PCI DSS, POPIA, and FICA.</p>', unsafe_allow_html=True)
        
if choice == 'Login':
    if st.session_state.keep_graphics == True:
                # reading csv
                error_df = pd.read_csv('results_df.csv')
                error_df.columns = ['Index', 'Target variable', 'Score']
                error_df = error_df[['Target variable', 'Score']]

                # creating threshold slider
                st.title("Fraud Detection Dashboard")
                threshold = st.slider("Threshold (default of 50%)", min_value=0.00, max_value=1.00, step=0.05, value=0.50)
                threshold_df, metrics, metrics_default = get_metrics_df(error_df, threshold=threshold)

                # input box for cost, then display total cost of fraud
                number1 = st.number_input('Cost of correctly detecting fraud') # true positive
                number2 = st.number_input('Cost of incorrectly classifying normal transactions as fraudulent') # false positive
                number3 = st.number_input('Cost of not detecting fraudulent transactions') # false negative
                number4 = st.number_input('Cost of correctly detecting normal transactions') # true negative

                # setting cost defaults
                tp_default = 0
                fp_default = 0
                fn_default = 0
                tn_default = 0

                for i, row in threshold_df.iterrows():
                    if row['Target variable'] == 1 and row['Classification_default'] == 1:
                        tp_default += 1
                    elif row['Target variable'] == 0 and row['Classification_default'] == 1:
                        fp_default += 1
                    elif row['Target variable'] == 1 and row['Classification_default'] == 0:
                        fn_default += 1
                    elif row['Target variable'] == 0 and row['Classification_default'] == 0:
                        tn_default += 1
                st.write('The default cost of fraud is ', (number1 * tp_default) + (number2 * fp_default) + (number3 * fn_default) + (number4 * tn_default))

                tp = 0
                fp = 0
                fn = 0
                tn = 0

                for i, row in threshold_df.iterrows():
                    if row['Target variable'] == 1 and row['Classification'] == 1:
                        tp += 1
                    elif row['Target variable'] == 0 and row['Classification'] == 1:
                        fp += 1
                    elif row['Target variable'] == 1 and row['Classification'] == 0:
                        fn += 1
                    elif row['Target variable'] == 0 and row['Classification'] == 0:
                        tn += 1
                st.write('The updated cost of fraud is ', (number1 * tp) + (number2 * fp) + (number3 * fn) + (number4 * tn))

                # updated
                metrics.loc[len(metrics.index)] = ['Number of fraudulent transactions detected', tp, '']
                metrics.loc[len(metrics.index)] = ['Number of fraudulent transactions not detected', fn, '']
                metrics.loc[len(metrics.index)] = ['Number of good transactions classified as fraudulent', fp, '']
                metrics.loc[len(metrics.index)] = ['Number of good transactions classified as good', tn, '']
                metrics.loc[len(metrics.index)] = ['Total number of transactions assessed', tp + fp + fn + tn, '']
                st.dataframe(metrics.assign(hack="").set_index("hack"))
                # default
                # `metrics_default` is a DataFrame that is being used to store and display the default
                # metrics related to fraud detection. These default metrics are calculated based on
                # the default classification results before any user input for cost adjustments. The
                # DataFrame `metrics_default` is populated with the following information:
                # - Number of fraudulent transactions detected
                # - Number of fraudulent transactions not detected
                # - Number of good transactions classified as fraudulent
                # - Number of good transactions classified as good
                # - Total number of transactions assessed
                metrics_default.loc[len(metrics_default.index)] = ['Number of fraudulent transactions detected', tp_default, '']
                metrics_default.loc[len(metrics_default.index)] = ['Number of fraudulent transactions not detected', fn_default, '']
                metrics_default.loc[len(metrics_default.index)] = ['Number of good transactions classified as fraudulent', fp_default, '']
                metrics_default.loc[len(metrics_default.index)] = ['Number of good transactions classified as good', tn_default, '']
                metrics_default.loc[len(metrics_default.index)] = ['Total number of transactions assessed', tp_default + fp_default + fn_default + tn_default, '']
                st.dataframe(metrics_default.assign(hack="").set_index("hack"))
                
    st.session_state.selected_option = 'A'
    #st.session_state.access == False
    if st.session_state.keep_graphics == True:
        st.session_state.hide = True
    else:
        st.session_state.hide = False
        
    
    login = st.sidebar.button('Login')
    if login or st.session_state.keep_graphics:
        if len(email) == 0:
            st.error("To Login: Valid Registered Email Address is required.")
            st.stop()            
        elif len(password) == 0:
            st.error("To Login: Valid Registered Password is required.")
            st.stop()
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.selected_option = '100'
                st.session_state.keep_graphics = True                 
                
            except:
                st.error('Login failed. Only registered user profile can access the Credit Card Fraud Detection Dashboard!')

    if choice == 'Login' and st.session_state.selected_option == "A" and st.session_state.hide == False:
        st.header("Detecting Your Transactions with :blue[Advanced Fraud Detection] :male-detective:", divider='gray')
        st.markdown("""
        <style>
        .big-font {
            font-size:18px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<p class="big-font">Learn from new data and AI-powered analytics to safeguard your financial operations.</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="big-font">Main Features </h>', unsafe_allow_html=True)
        st.markdown('<h2 class="big-font">Intelligent Protection: </h>', unsafe_allow_html=True)
        st.markdown('<p class="big-font">Our system employs cutting-edge machine learning algorithms to identify suspicious patterns and anomalies in transaction data, before it impacts your business. </p>', unsafe_allow_html=True)
        st.markdown('<h2 class="big-font">Comprehensive Dashboard: </h>', unsafe_allow_html=True)
        st.markdown('<p class="big-font">Monitor transaction patterns, fraud attempts, and security metrics through an intuitive visual interface designed for both technical and non-technical users. </p>', unsafe_allow_html=True)
            
    