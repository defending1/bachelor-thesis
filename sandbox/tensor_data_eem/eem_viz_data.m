%% Visualizing the tensor data directly
% Each slice represents a mixture

%% Choose raw data or filled in data
slices = 1:18;
T = X(slices,:,:);
figid = 2;

%% Raw data, with some missing entries

figure(figid); clf; 
mm = 3;
nn = ceil(size(T,1)/mm);
for i = 1:size(T,1)
    YY = mode_ranges{2};
    XX = mode_ranges{3};
    ZZ = double(squeeze(T(i,:,:)));    
    subplot(mm,nn,i);
    %zlevs = [0:1e5/2:750000];
    %zlevs = [0 quantile(T(:),[0.1:0.1:0.5]) quantile(T(:), [0.6:0.025:1])];
    %zlevs = [min(T(:)) quantile(T(:),[0.05:0.05:1])]
    zlevs = linspace(-1.1e4, 7e5, 20);
    contourf(XX,YY,ZZ,zlevs);
    xlabel(sprintf('%s (nm)', lower(mode_titles{3})))
    ylabel(sprintf('%s (nm)', lower(mode_titles{2})))
    zlabel('fluorescence intensity');
    xlim([XX(1), XX(end)])
    ylim([YY(1), YY(end)])
    title(sprintf('Mix [ %4.2f %4.2f %4.2f]', mixtures(i,:)))
    %axis equal
end

%% Viz Decomp Nicely
rng('default')
M = cp_als(T,3);
score(ktensor({M.U{1}}),ktensor({mixtures(slices,:)}),'lambda_penalty',false)
%%
hh = viz(M,'PlotCommands',{'bar','plot','plot'},'ModeTitles',modes)

%% Overwrite Mode-1 with true versus computed factorizations
A = M.U{1};
B = mixtures(slices,:);
B = bsxfun(@rdivide,B,sqrt(sum(B.^2,1))); %<- Normalize
[sc,tmp] = score(ktensor({B}),ktensor({A}),'lambda_penalty',false)
Bp = tmp.U{1};
AB = [A B];
yl = [min( -0.01, min(AB(:)) ), max( 0.01, max(AB(:)) )];

for j = 1:3
    hold(hh.FactorAxes(1,j),'off');
    axes(hh.FactorAxes(1,j));
    bar([A(:,j) Bp(:,j)], 'grouped')
    ylim(hh.FactorAxes(1,j),yl);
    set(hh.FactorAxes(1,j),'Ytick',[]);
    if j == 1
        legend('Computed','True');
    end
    if j < 3
        set(hh.FactorAxes(1,j),'XtickLabel',{});
    end
end

