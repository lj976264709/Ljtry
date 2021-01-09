function Threshold=Fun_OTSU(Img)
%% 大律法
%所有灰度序列
gray=Img(:);
%求各个灰度值出现的频率（1：255）
Frequency=zeros(1,255);
for i=1:length(gray)
    gray_temp=gray(i);
    if gray_temp>0
        Frequency(gray_temp)=Frequency(gray_temp)+1;
    end
end
%计算
OTSU=0;
OTSU0=0;
OTSU_t0=0;
Gray_p=zeros(1,255);
su=sum(Frequency);%计算出灰度的总和
for i=1:255
    Gray_p(i)=Frequency(i)/su;%计算出每一个灰度值在图像中出现的概率，对应公式中的P(i)
end
for i=1:255
    Foward_p=sum(Gray_p(1:i));
    %计算前景的灰度概率和,对应公式中的W0
    Back_p=sum(Gray_p(i+1:255));
    %计算后景的灰度概率和,对应公式中的W1
    Omega_f=sum((1:i).*Gray_p(1:i))/Foward_p;
    %计算出前景的平均灰度,对应公式中的μ0
    Omega_b=sum((i+1:255).*Gray_p(i+1:255))/Back_p;
    %计算出后景的平均灰度,对应公式中的μ1
    Omega=Foward_p*Omega_f+Back_p*Omega_b;
    %计算出整幅图像的平均灰度对应公式中的μT
    OTSU0=(Omega_f-Omega)^2*Foward_p+(Omega_b-Omega)^2*Back_p;
    %计算出前景和背景的方差，对应公式中的μB
    if OTSU<OTSU0
        OTSU=OTSU0;%一旦找到更大的方差即更新
        OTSU_t0=i;%找到公式中的K*,即最佳阈值
    end
end
Threshold=OTSU_t0;
end