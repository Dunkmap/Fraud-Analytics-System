from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'Code Architecture & Real-Time Setup Analysis', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, num, label):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, f'Section {num}: {label}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 12)
        # Replacing unicode characters with simpler ones or using multi_cell directly.
        # FPDF standard helvetica handles ascii/latin strictly. Hinglish string should use basic letters.
        self.multi_cell(0, 8, text)
        self.ln(5)

    def add_section(self, num, title, body):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(body)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

body_1 = """(English)
No, this is NOT a real-time system. A real-time system processes data instantaneously as soon as it is generated (e.g., using technologies like Apache Kafka, RabbitMQ, WebSockets, or live streaming APIs). 
In this project, the data is loaded from static CSV files ('final_dataset.csv', 'transactions.csv') which contains historical transaction data. The Streamlit app filters and visualizes this prepared historical data.

(Hinglish)
Nahi, yeh ek real-time system nahi hai. Kisi bhi real-time system me data generate hote hi turant process hota hai (jaise ki Kafka, WebSockets ya live streaming APIs ka use karke). 
Is project me, data pehle se bacha hua aur process kiya hua static CSV files se load kiya ja raha hai ('final_dataset.csv'). Streamlit app isi historical data ko filter kar ke visualize kar raha hai."""

body_2 = """(English)
If it is not real-time, then it is a "Batch Processing Data Analytics and Risk Intelligence Dashboard". 
It's a static interactive web dashboard built with Streamlit that processes historical data for fraud analysis and displays key performance indicators and patterns.

(Hinglish)
Agar yeh real-time nahi hai, toh ye ek "Batch Processing Analytics Dashboard" ya "Static Analysis Tool" hai. 
Yeh Streamlit ki madad se banaya gaya ek interactive web application hai jo purane historical data pe analysis karta hai, graph plot karta hai, aur fraud patterns ko dashboard par report karta hai."""

body_3 = """(English)
1. Data Preparation: The dataset is cleaned, encoded, and prepared using standard Pandas operations found in 'Creating_Dataset.ipynb'.
2. Machine Learning: The model handles imbalanced class distributions via SMOTE (Synthetic Minority Over-sampling Technique) and evaluates fraud detection using Scikit-Learn models like RandomForest and LogisticRegression in 'Machine_learning_part.ipynb'.
3. Dashboarding: The 'app.py' script brings it all together using Streamlit for layout/UI and Plotly for rich interactive visualizations (Fraud by Merchant, Risk Score Distribution, Geographic maps).

(Hinglish)
1. Data Preparation: Sabse pehle 'Creating_Dataset.ipynb' me data ko clean aur merge kiya gaya hai using Pandas.
2. Machine Learning Pipeline: 'Machine_learning_part.ipynb' file me credit card fraud data ke imbalance ko SMOTE se balance kiya gaya hai, aur phir RandomForest, Logistic Regression jaise ML models ko evaluate kiya gaya hai.
3. Dashboard Presentation: 'app.py' ek bohat attractive UI banata hai Streamlit aur custom CSS features (3D hover, gradient colors) ke sath. Plotly ka use statistical insights dikhane ke liye kiya hai."""

body_4 = """(English)
Yes, it is a very good fundamental approach for a Proof of Concept (PoC) or academic level risk intelligence product.
- Why is it good? The use of SMOTE effectively handles the extreme class imbalance typically seen in fraud detection. 
- The user interface is well structured and extremely pleasant with customized CSS gradients and dynamic Plotly charts.
- How to improve it to real-time? You would need to add a message broker like Apache Kafka to stream live transactions, connect to a database (like PostgreSQL/MongoDB) rather than CSV files, and deploy a REST API (using FastAPI/Flask) that scores live transactions against a saved ML model pickle file.

(Hinglish)
Haan, yeh ek bahut badhiya approach hai agar ye Proof of Concept (PoC) ya college/portfolio project hai!
Kyun aur Kaise?
- Kyunki isme fraud classification ki sabse badi problem 'Imbalanced Data' ko SMOTE se acche se handle kiya gaya hai. UI ke terms mein, Custom CSS, 3D floating credit cards aur Plotly graphs application ko ekdum premium feel dete hain.
- Isse REAL-TIME banayenge kaise? Enterprise level par, isme Apache Kafka ya RabbitMQ daalna padega jisse live transaction stream ho sake, aur static CSV views hata kar PostgreSQL ya MongoDB database connect karna hoga. Model inference ke liye FastAPI ya Flask jaisi API banani hogi."""

pdf.add_section(1, "Is it a Real-Time System?", body_1)
pdf.add_section(2, "What is it then?", body_2)
pdf.add_section(3, "What is its Approach?", body_3)
pdf.add_section(4, "Is it good? How?", body_4)

pdf.output('System_Analysis.pdf')
print("Successfully created System_Analysis.pdf")
