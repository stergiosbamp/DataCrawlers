# -*- coding: utf-8 -*-

""" Parse excel files into correct format in csv files. """
""" """
"""	Data are stored in an excel file named antalya_cutler_all_data_ (version 1).xlsx in different sheets """
""" Sheet name:

	- ECON_SHOP_RENT
	- No-ECON_EMPLOYERS
	- No-ECON_GENERAL ELECTIRICK
	- No-ECON_WATER POMP ELECTIRIC
	- No-ECON_DUDENZONE HOUSING INDEX
	- No-TRANSPORT_VML55A, TRANSPORT_VC56, TRANSPORT_KC35, TRANSPORT_KC35A, TRANSPORT_CV17A, TRANSPORT_MZ78, TRANSPORT_MK80, TRANSPORT_MK80A, TRANSPORT_VF66
"""
""" Original files must be previously saved in folder temp"""
""" """
""" code: anta_eco_citiofantalya_ShopsRentEarn_year """



import os
import pandas as pd
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


code= 'anta_eco_citiofantalya_ShopsRentEarn_year' 

l_temp_path = './temp/'
l_final_path = './data/'
data_sheetn = 'ECON_SHOP_RENT'

xlfname = 'antalya_cutler_all_data_ (version 1).xlsx'


class anta_eco_ShopsRentEarn_year(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (data_sheetn,header = 1,usecols='A:B')

		#remove index columns
		df_data.reset_index(inplace = True)

		
		df_data.rename(columns={df_data.columns[1]:'Year',df_data.columns[2]:'shop_rent'},inplace=True)

		df_data = df_data[['Year','shop_rent']].copy()


		#save
		
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code)
		fullname = os.path.join(outdir, csvfile)

		df_data.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
	a = anta_eco_ShopsRentEarn_year()
	a.parse_file()	
