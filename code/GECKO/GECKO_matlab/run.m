model = readSBML('../../data/model/iML1515.xml',1000);
ravmodel = saveECmodel(model,'COBRA','eco','v1');
[swissprot,kegg] = buildProtDatabase();
model_data = getEnzymeCodes(model);
kcats = matchKcats(model_data, 'Escherichia coli K-12 MG1655');

scmodel = readSBML('E:\\20191218\\酶约束模型自动化\\GECKO-master\\models\\ecYeastGEM\\ecYeastGEM.xml',1000);

newModel=ravenCobraWrapper(model)