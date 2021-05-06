function centriod_num=cv(picturefile,d,a,b)%图片路径，图片处理结果位置，筛选距离，迭代次数，膨胀收缩系数

%% 读取影像
Img=imread(picturefile);
Img=uint8(Img);
Img_T = Img;
%% 指数计算 -- 绿色植被指数
Img_GVI=Img;
% figure('name','原始影像','color','w');
% imshow(Img);title('原始影像');
%% 灰度化
Img_gray=Img_T;
Img_gray=uint8(Img_gray);
%% 5*5 高斯滤波去除噪声
filter = fspecial('gaussian',[3,3],1); 
Img_Gauss = imfilter(Img_gray, filter, 'replicate');
filter = fspecial('average',[3,3]); 
Img_Gauss = imfilter(Img_Gauss, filter);
%% 大律法（OTSU）二值化（存在问题，需对植被区域进行二值化，选取阈值时，应根据植被区域灰度选取）
Threshold=Fun_OTSU(Img_Gauss);
Img_O=double(Img_Gauss);
Img_O(Img_O<=Threshold)=0;
Img_O(Img_O>Threshold)=1;
%% 局部最大值
Result_Max=imregionalmax(Img_Gauss,8);

%% 获取局部最大值的各个连通域
L = bwlabel(Result_Max,8);
RGB = label2rgb(L);
%% 获取各联通区域的重心
stats = regionprops(Result_Max, 'basic');
centroids = cat(1, stats.Centroid);
Dist=pdist(centroids);
Dist2 = squareform(Dist);
%% 剔除距离小于D的点
%D=4;
[Num]=Fun_Select_Point(Dist2,d,Img_T,centroids);
Result_Max_F=Result_Max;
for i=1:length(Num)
    Result_Max_F(L==Num(i))=0;
end
se=strel('disk',3);%圆盘型结构元素
Result_Open = imopen(Result_Max_F,se);  %开运算
Result_Close=imclose(Result_Max_F,se);%先开后闭运算
%% cv模型
bw = activecontour(Img_Gauss,Result_Max_F,a,'Chan-Vese','ContractionBias',b);%迭代次数
% figure('name','snake主动轮廓','color','w');
% imshow(bw);title('主动轮廓');
%% 获取边缘,展示结果
contour = double(bwperim(bw)); 
[L,num] = bwlabel(bw,4);
centriod_num=[];
for i=1:num%将各个连通域的质心输出到数组中
    stats = regionprops(L ==i, 'all');
    centriods= stats.Centroid;
    centriod_num(i,1)=centriods(1);
    centriod_num(i,2)=centriods(2);
end
% %%
% xlswrite('tree_test3.tif_cv.xls',centriod_num,1,'F1')
%%
%%imshow(L)
%%imshow(L)
f=contour*255;
f=uint8(f);

% figure('name','result','color','w');
result = imadd(0.8*Img,f);
% imshow(result);
%imwrite(result,presult);