import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



class DLIS_reader:
    """
    Source : https://towardsdatascience.com/loading-well-log-data-from-dlis-using-python-9d48df9a23e2
    Author : Andy Mcdonald
    """
    def __init__(self,file_path):
        self.file_path = file_path
    def DLIS_describe(self):
        from dlisio import dlis
        f, *tail = dlis.load(self.file_path)
        return(f.describe())
    def Well_data(self):
        from dlisio import dlis
        f, *tail = dlis.load(self.file_path)
        origin, *origin_tail = f.origins
        return(origin.describe())
    def summary_channels(self):
        from dlisio import dlis
        import pandas as pd
        f, *tail = dlis.load(self.file_path)
        df = pd.DataFrame()
        kwargs = {"name":'Name', "long_name":'Long Name',"dimension":'Dimension', "units":'Units', "frame":'Frame'}
        for i, (key, value) in enumerate(kwargs.items()):
            list_of_values = []
            # Iterate over each parameter and get the relevant key
            for item in f.channels:
                # Account for any missing values.
                try:
                    x = getattr(item, key)
                    list_of_values.append(x)
                except:
                    list_of_values.append('')
                    continue
            # Add a new column to our data frame
            df[value]=list_of_values
        # Sort the dataframe by column 1 and return it
        return df.sort_values(df.columns[0])
    def DLIS_dataframe (self,lista):
        from dlisio import dlis
        import pandas as pd
        f, *tail = dlis.load(self.file_path)
        frame1 = f.object('FRAME','0')
        curves = frame1.curves()
        df = pd.DataFrame()
        for elements in lista:
            if elements == "DEPTH":
                df[elements] = curves[elements]*0.00254
            else : 
                df[elements] = curves[elements]
        return(df)

    
    
def plot_prod(df,wells_list,type_well):
    fig = plt.figure(figsize=(20,10),dpi=200)
    for well in wells_list:
        df_temp = df[ df["NPD_WELL_BORE_NAME"] == well ]
        if type_well == "prod":
            plt.scatter(df_temp["DATEPRD"],df_temp["BORE_OIL_VOL"],label=well,s=8)
        else :
            plt.scatter(df_temp["DATEPRD"],df_temp["BORE_WI_VOL"],label=well,s=8)
    plt.xlabel("Date")
    if type_well == "prod":
        plt.ylabel("Produccion[stbd]")
        plt.title("Produccion por pozo")
    else:
        plt.ylabel("Inyeccion[stbd]")
        plt.title("Inyeccion por pozo")
    plt.legend()
    plt.show()
    
def well_log_plt (df,logs) :
    fig,axes = plt.subplots(len(logs),1,figsize=(15,8),sharex=True)
    for i,log in enumerate(logs):
        axes[i].scatter(df["DATEPRD"],df[log],s=1.5)
        axes[i].set_ylabel(log)
    axes[i].set_xlabel("Fecha")
    plt.tight_layout()

