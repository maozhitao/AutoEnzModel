
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [uni,EC,MW,genes] = addMultipleMatches(uni,EC,MW,genes,conflicts,DB)
for i=1:length(conflicts{1})
    indexes = conflicts{2}{i};
    for j=2:length(indexes)
        indx  = indexes(j);
        uni   = [uni; DB{indx,1}];
        ECset = getECstring('',DB{indx,4});
        EC    = [EC; {ECset}];
        MW    = [MW; DB{indx,5}];
        genes = [genes; conflicts{1}{i}];
    end
end
end