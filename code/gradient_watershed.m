%梯度分水岭Python调用
%% 
function centriod_num=gradient_watershed(filename,a,b)%图片路径，腐蚀系数，膨胀系数
%% 

% filename='D:\研究生\实验\图片对比实验\卫星影像\tree_test2.tif实验\tree_test2_exg.tif';
f=imread(filename);
Info=imfinfo(filename);
if Info.BitDepth>8    
f=rgb2gray(f);
end
%figure,
%mesh(double(f));%显示图像，类似集水盆地
%方法2：使用梯度的两次分水岭分割，从结果可以看出还存在过分割问题（在方法1的基础上改进）
h=fspecial('sobel');%获得纵方向的sobel算子
fd=double(f);
g=sqrt(imfilter(fd,h,'replicate').^2+imfilter(fd,h','replicate').^2);%使用sobel算子进行梯度运算
l=watershed(g);%分水岭运算
% imshow(l);
wr=l==0;    
%此处需要设置参数，此处使用1，3
se=strel('disk',a);
 %g2=imclose(imopen(g,ones(3,3)),ones(3,3));%进行开闭运算对图像进行平滑
g2=imclose(imopen(g,se),ones(b,b));%进行开闭运算对图像进行平滑
l2=watershed(g2);%再次进行分水岭运算
wr2=l2==0;f2=f;
f2(wr2)=255;
%%
contour = double(bwperim(l2)); %寻找二值图的边缘
f1=contour*255;
[L,num] = bwlabel(l2,4);%对边缘进行标记,L将不同连通域进行标记，num表示连通域的个数

for i=1:num%将各个连通域的质心输出到数组中
    stats = regionprops(L ==i, 'all');
    centriods= stats.Centroid;
    centriod_num(i,1)=centriods(1);
    centriod_num(i,2)=centriods(2);
end
%%
%figure
%imshow(f2);