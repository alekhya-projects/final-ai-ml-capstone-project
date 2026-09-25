import pandas as pd
#Read raw data
df=pd.read_csv("data_pipeline/raw_books.csv")
print("Original Dataset")
print(df.head())
print("Total Books:",len(df))

#clean price
df["price_gbp"]=(df["price"].astype(str).str.replace("£","",regex=False).str.replace(",","",regex=False).str.strip())
df["price_gbp"]=pd.to_numeric(df["price_gbp"],errors="coerce")
#convert ratings
rating_map={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
df["rating"]=df["star_rating"].map(rating_map)
 
#Convert Availability into True/False
df["in_stock"] =df["availability"].astype(str).str.contains("In stock",case=False,na=False).astype(int)  

#GRB to INR
GRB_TO_INR=105.50
df["price_inr"]=df["price_gbp"]*GRB_TO_INR

#Remove missing ratings
df=df.dropna(subset=["rating"])

#Fill missing numeric values with median(if any)
df["price_gbp"]=df["price_gbp"].fillna(df["price_gbp"].median())
df["price_inr"]=df["price_inr"].fillna(df["price_inr"].median())

#Final columns
cleaned_df=df[["title","category","price_gbp","price_inr","rating","in_stock"]]

#save cleaned csv
cleaned_df.to_csv("data_pipeline/cleaned_books.csv",index=False)
print("Cleaned dataset saved successfully!")

print(cleaned_df.head())
print("Total Clean Books:",len(cleaned_df))