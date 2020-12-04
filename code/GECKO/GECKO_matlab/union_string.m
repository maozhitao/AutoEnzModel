%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function str = union_string(cell_array)
%Receives any 1xn cell array and returns the union of all non empty
%elements as a string
nonempty = ~cellfun(@isempty,cell_array);
str      = strjoin(cell_array(nonempty)',' ');
end