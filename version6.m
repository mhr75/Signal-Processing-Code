%Annotation calculation
clear all
close all
clc;
matfiles=dir(fullfile('X:\thesis rimu\Group6_MindWandering\CSVFiles\*.csv'));  %reading the files
numfids = length(matfiles); %files length 
fs=1024; 

DURATION= [29.65 31.38 29.11 33.77 29.38 29.27 28.95 28.77 30.89];
MINDWANDERING=[19 25 23 34 25 21 26 29 36];
BEFOREMW=[60.30 46.12 49.14 33.69 47.39 55.48 44.06 40.95 32.43];

for ii =1:1
    fprintf('.');  
    [dataEEG,header] = importdata(strcat('X:\thesis rimu\Group6_MindWandering\CSVFiles\', matfiles(ii).name));
    channels=[1:64];
    addChannelDataAll=[];
    MAD=[];
    
    total_duration_bMW=MINDWANDERING(ii)*(BEFOREMW(ii)/60);
    total_MW_duration=DURATION(ii)-total_duration_bMW;
    mean_duration=(total_MW_duration/MINDWANDERING(ii))*60;
    disp(mean_duration);
    %disp(mean_duration);
    %disp(MINDWANDERING(ii));
    %disp('-----------');
    startingTime=[];
    endingTime=[];
    start=BEFOREMW(ii);
    for jj=1:MINDWANDERING(ii)
        startingTime=[startingTime start];
        %endingSecond=(startingTime(jj)+mean_duration);
        endingTime=[endingTime (startingTime(jj)+mean_duration)];
        start= endingTime(jj)+BEFOREMW(ii);
        %disp(startingTime(jj));
        %disp(endingTime(jj));
    end
    [m,n]=size(dataEEG.data);
    %disp(m);
    totalLen=round(m/fs);
    step=1;
    sizeOfMW=length(startingTime);
    for k=1:totalLen 
        if(sizeOfMW<step)MAD=[MAD;0];
        else
        a=round(startingTime(step));
        b=round(endingTime(step));
        %disp(a);
        %disp(b);
        %disp('---');
        %disp(k);
        if(k>=a && k<=b)
            %disp('yee');
            MAD=[MAD;1];
            if (b==k)step=step+1;
            end            
        else
            MAD=[MAD;0];
        end
        end
    end
        
    
    for j=1:length(channels)
        
        startt=2;
        endd=1025;
        addChannelData=[];
        
        
        for k=1:totalLen
            %fprintf('%d',totalLen);
            f1 = kurtosis(dataEEG.data(startt:endd,j));
            f2 = skewness(dataEEG.data(startt:endd,j));
            f3=std(dataEEG.data(startt:endd,j));  
            f4=mean(dataEEG.data(startt:endd,j));
            f5=max(dataEEG.data(startt:endd,j));
            f6=min (dataEEG.data(startt:endd,j));
            sumValues=sum((dataEEG.data(startt:endd,j)).^2);
            f7= sumValues/1024;
           % f7=graycoprops((dataEEG.data(startt:endd,j)),{'energy'} );
          %  f8=entropy(dataEEG.data(startt:endd,j));
            fea=[ f1 f2 f3 f4 f5 f6 f7];
            addChannelData=[addChannelData;fea];
            startt=endd+1;
            endd=fs*(k+1); 
        end
        
        addChannelDataAll=[addChannelDataAll addChannelData];
        
    end
   % addChannelDataAll=normalize(addChannelDataAll,'range'); % comment out if you want without normalize value
    %addChannelDataAll=[addChannelDataAll MAD];
    cHeader=[];
    for iterateHeader=1:64
        a= strcat('kurtosis',int2str(iterateHeader));
        b= strcat('skewness',int2str(iterateHeader));
        c= strcat('std',int2str(iterateHeader));
        d= strcat('mean',int2str(iterateHeader));
        e=strcat('max',int2str(iterateHeader));
        f=strcat('min',int2str(iterateHeader));
        g=strcat('energy',int2str(iterateHeader));
        cHead={a,b,c,d,e,f,g};
        
       % cHead={a,b,c,d,e,f,g};
        cHeader=[cHeader cHead];    
    end
    commaHeader = [cHeader;repmat({','},1,numel(cHeader))]; %insert commaas
    commaHeader = commaHeader(:)';
    textHeader = cell2mat(commaHeader); %cHeader in text with commas
    %write header to file
    fid = fopen(strcat('X:\thesis rimu\Group6_MindWandering\Task',num2str(ii),'.csv'),'w'); 
    fprintf(fid,'%s\n',textHeader);
    fclose(fid);
    dlmwrite(strcat('X:\thesis rimu\Group6_MindWandering\Task',num2str(ii),'.csv'),addChannelDataAll,'-append');
    
    newMean=[];
    for iii=1:totalLen
        newKur=[];
        newSke=[];
        newStd=[];
        newMena=[];
        newMax=[];
        newMin=[];
        newEne=[];
        newKur=[newKur (addChannelDataAll(iii,1:7:64))];
        kurz=mean(newKur);
        newSke=[newSke (addChannelDataAll(iii,2:7:64))];
        skez=mean(newSke);
        
        newStd=[newStd (addChannelDataAll(iii,3:7:64))];
        stdz=mean(newStd);
        newMena=[newMena (addChannelDataAll(iii,4:7:64))];
        menaz=mean(newMena);
        
        newMax=[newMax (addChannelDataAll(iii,5:7:64))];
        maxz=mean(newMax);
        newMin=[newMin (addChannelDataAll(iii,6:7:64))];
        minz=mean(newMin);
        
        newEne=[newEne (addChannelDataAll(iii,7:7:64))];
        enez=mean(newEne);
        meanvalues=[kurz skez stdz menaz maxz minz enez];
        newMean=[newMean;meanvalues];
    end
    newMean=normalize(newMean,'range');
    newMean=[newMean MAD];
    cHeaderz={ 'kurtosis', 'skewness', 'std', 'mean','max','min','energy','MindWandering' };
    commaHeaderz = [cHeaderz;repmat({','},1,numel(cHeaderz))]; %insert commaas
    commaHeaderz = commaHeaderz(:)';
    textHeaderz = cell2mat(commaHeaderz);
    fid2 = fopen(strcat('X:\thesis rimu\Group6_MindWandering\Tasks',num2str(ii),'.csv'),'w'); 
    fprintf(fid2,'%s\n',textHeaderz);
    fclose(fid);
    dlmwrite(strcat('X:\thesis rimu\Group6_MindWandering\Tasks',num2str(ii),'.csv'),newMean,'-append');
    
end  

fprintf('end');