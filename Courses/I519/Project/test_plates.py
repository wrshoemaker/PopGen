from FlowCytometryTools import FCPlate

plate = FCPlate.from_dir(ID='Demo Plate', path= './20151203/CTC_FVD_Hoechst_test120315', parser='name')
print plate
