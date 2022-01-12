name='rqdec.txt';
[data]=textread(name);
[r,c] = size(data);
data=data(:,1:c-1);
f=fopen('infsym.txt','w');

for i = 1:(r/4)
    disp(i)
    received=rot90(rot90(rot90(data(i*4-3,:))));
    
    lossi=rot90(rot90(rot90(data(i*4-2,:))));
    lossi(find(lossi==0))=[];
    
    repsym=rot90(rot90(rot90(data(i*4-1,:))));
    repsym(find(lossi==0))=[];
    
    repairindex=data(i*4,:);
    repairindex(find(lossi==0))=[];
    
    decoded=RaptorDecoder(received,160,lossi,repsym,repairindex,0)
    decoded=rot90(decoded)
    decoded=decoded(:,1:160)
    length=size(decoded,2);

    %record decoded information symbols
    for j = 1:length
        fprintf(f,'%d',decoded(1,j));
        fprintf(f,' ');
    end;
    fprintf(f,'\n');
    
end

fclose(f);
