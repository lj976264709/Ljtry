function [Num]=Fun_Select_Point(Dist,D,GVI,centroids)
%% 寻找间距小于指定值D的点,并根据GVI的值判断哪些点该剔除。返回的是需要被剔除的点
Dist(Dist==0)=NaN;
[R,C]=find(Dist<D);
Num=nan(1,length(R));
if isempty(R)
    Num=[];
else
    for i=1:length(R)
        Point_R=floor(centroids(R(i),:));
        Point_C=floor(centroids(C(i),:));
        GVI_R=GVI(Point_R);
        GVI_C=GVI(Point_C);
        if GVI_R>=GVI_C
            Num(i)=C(i);
        else
            Num(i)=R(i);
        end
    end          
end
Num=unique(Num);
end