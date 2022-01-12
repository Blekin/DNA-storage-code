%read information symbols and primary repair symbols
name='inf_pri_new.txt';
[data]=textread(name);
[r,c] = size(data);
f=fopen('sRepSym.txt','w');

%generating secondary repair symbols for each row
for i = 1:r
    [ SourceSymbols, RepairSymbols, numSouceSymbols, numPadding ] = RaptorEncoder_new( data(i,:), 0.9975, 0 );
    repsym=rot90(RepairSymbols);
    length=size(repsym,2);

    %record secondary repair symbols
    for j = 1:length
        fprintf(f,'%d',repsym(1,j));
        fprintf(f,' ');
    end;
    fprintf(f,'\n');
    
end;

fclose(f);