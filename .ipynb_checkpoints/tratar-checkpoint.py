def ref_title(df_origin, df):
    df_origin["Title"] = df_origin.Name.str.extract(r"([A-Za-z]+)\.")
    
    # funções para diminuir a quantidade valores unicos
    Mlle_Miss_Mme = lambda x: "Miss" if x.lower() in "Mlle_Miss_Mme_Countess_Lady_Ms".lower().split("_") else x
    Other = lambda x: "Othet" if x.lower() not in "Mr, Mrs, Miss".lower().split(", ") else x
    
    df_origin.Title = df_origin.Title.apply(Other)
    df_origin.Title = df_origin.Title.apply(Mlle_Miss_Mme)
    
    # encoder applie
    df_origin.loc[:, "Title"] = title_encoder.transform(df_origin.Title)
    
    # applied on train and test dataframe 
    df["Title"] = df_origin["Title"]


def ref_sex(df_origin, df):
    df["Male"] = sex_encoder.transform(df_origin[["Sex"]])


def ref_cabin_num(df_oring, df):
    df["Cabin_num"] = df_oring.Cabin.apply(lambda x: 0 if pd.isna(x) else len(x.split(" ")))


def ref_cabin_let(df_origin, df):
    df_origin["Cabin_let"] = df_origin.Cabin.apply(lambda x: "0" if pd.isna(x) else  str(x)[0])
    col_name = ["Cabin_"+name for name in cabin_ecoder.classes_]
    cabin_code = pd.DataFrame(cabin_ecoder.transform(data.Cabin_let), columns=col_name).drop(columns=col_name[1])
    for feature in cabin_code.columns:
        df[feature] = cabin_code[feature]

def ref_embarked(df_origin, df):
    df_origin.Embarked.fillna("S", inplace=True)
    col_name = ["Embaked_"+name for name in embarked_encoder.classes_]
    emarked_code = pd.DataFrame(embarked_encoder.transform(df_origin.Embarked), columns=col_name).drop(columns=col_name[0])
    for feature in emarked_code.columns:
        df[feature] = emarked_code[feature]
        
        
def ref_age(df_origin, df):
    for sex, pclass in [(sex, pclass) for sex in df_origin.Sex.unique() for pclass in df_origin.Pclass.unique()]:
        condition = (df_origin.Sex == sex) & (df_origin.Pclass == pclass)
        age_mean = df_origin.loc[condition, "Age"].mean()
        df_origin.loc[condition & df_origin.Age.isnull(), "Age"] = age_mean
    
    df["Age"] = df_origin.Age


def ref_fare(df_origin, df):
    ref_cabin_num(df_origin, df_origin)
    for pclass, cabin_num in [(pclass, cabin_num) for pclass in df_origin.Pclass.unique() for cabin_num in df_origin.Cabin_num.unique()]:
        condition = (df_origin.Pclass == pclass) & (df_origin.Cabin_num == cabin_num)
        fare_mean = df_origin.loc[condition, "Fare"].mean()
        df_origin.loc[condition & df_origin.Fare.isnull(), "Fare"] = fare_mean
    df["Fare"] = df_origin.Fare


def ref_pclass(df_origin, df):
    df["Pclass"] = df_origin.Pclass

    
def ref_sibsp(df_origin, df):
    df["SibSp"] = df_origin.SibSp

    

def ref_parch(df_origin, df):
    df["Parch"] = df_origin.Parch

    
def ref_family(df_origin, df):
    df["Family_size"] = df_origin.Parch + df_origin.SibSp


def ref(df_origin):
    df_origin = pd.DataFrame(df_origin)
    df = pd.DataFrame()
    ref_age(df_origin, df)
    ref_cabin_let(df_origin, df)
    ref_cabin_num(df_origin, df)
    ref_embarked(df_origin, df)
    ref_family(df_origin, df)
    ref_fare(df_origin, df)
    ref_parch(df_origin, df)
    ref_pclass(df_origin, df)
    ref_sex(df_origin, df)
    ref_sibsp(df_origin, df)
    ref_title(df_origin, df)
    return df
