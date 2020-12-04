%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function displayErrorMessage(conflicts,swissprot,kegg)
STR = '\n Some  genes with multiple associated proteins were found, please';
STR = [STR, ' revise case by case in the protDatabase.mat file:\n\n'];   
for i=1:length(conflicts{1})
    if strcmpi(conflicts{4}{i},swissprot)
        DB = swissprot;
    else
        DB = kegg;
    end
    proteins = DB(conflicts{3}{i},1);
    STR = [STR, '- gene: ' conflicts{2}{i} '  Proteins: ' strjoin(proteins) '\n'];
end
STR = [STR, '\nIf a wrongly annotated case was found then call the '];
STR = [STR, 'getEnzymeCodes.m function again with the option action'];
STR = [STR, '= ignore\n\n'];
STR = [STR, 'If the conflicting proteins are desired to be kept as isoenzymes'];
STR = [STR, ' then call the getEnzymeCodes.m function'];
STR = [STR, ' again with the option action = add\n'];
error(sprintf(STR))
end