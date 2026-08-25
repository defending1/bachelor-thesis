function viz_slices(T, mixtures, figid, fname)

if exist('figid','var')
    figure(figid); clf;
else
    figure;
end

mm = 3;
nn = ceil(size(T,1)/mm);
YY = 250:500;
XX = 210:5:310;
zlevs = linspace(-1.1e4, 7e5, 20);

for i = 1:size(T,1)
    ZZ = double(squeeze(T(i,:,:)));    
    subplot(mm,nn,i);
    contourf(XX,YY,ZZ,zlevs);    
    xlabel('excitation (nm)')
    ylabel('emission (nm)')
    zlabel('fluorescence intensity');
    xlim([XX(1), XX(end)])
    ylim([YY(1), YY(end)])
    if exist('mixtures','var')
        title(sprintf('Mix [%4.2f %4.2f %4.2f]', mixtures(i,:)))
    else
        title(sprintf('Sample %d',i));
    end
end

%%
width = 12;     % Width in inches
height = 10;    % Height in inches
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size

set(gcf,'InvertHardcopy','on');
set(gcf,'PaperUnits', 'inches');
papersize = get(gcf, 'PaperSize');
left = (papersize(1)- width)/2;
bottom = (papersize(2)- height)/2;
myfiguresize = [left, bottom, width, height];
set(gcf,'PaperPosition', myfiguresize);

%%
if exist('fname','var') && ~isempty(fname)
    print(fname,'-dpng','-r300');    
end