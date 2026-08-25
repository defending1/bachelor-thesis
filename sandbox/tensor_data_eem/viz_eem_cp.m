function sc = viz_eem_cp(M,M2,figid,fname,nrmval)
%VIZ_EEM_CP Visualization of CP for EEM data
%
%   VIZ_EEM_CP(M) visualizes the components of the Krusal tensor M which
%   corresponds to the EEM data tensor of size 18 x 251 x 21. The first
%   mode corresponds to samples and is plotted as a bar chart. The sceond
%   and third modes corresponds to exication and emissions, respectively,
%   and are plotted as lines with dots indicating each individual data
%   point. 
%
%   VIZ_EEM_CP(M,A1) takes A1, the true mixtures in a matrix of size 18 x 3
%   and plots those in the first component for comparison alongside the
%   first factor matrix.
%
%   VIZ_EEM_CP(M,Malt) takes another CP model and plots it together with
%   the first,
%
%   VIZ_EEM_CP(M,[],FIGID) uses the figure specified by FIGID. Anything can
%   be in the second argument.
%
%   VIZ_EEM_CP(M,[],FIGID,FNAME) saves the figure to the file FNAME.

%% Setup

% Fill in missing variables
if ~exist('M2','var')
    M2 = [];
end

if ~exist('figid','var')
    figid=[];
end

if ~exist('fname','var')
    fname = [];
end

if ~exist('nrmval','var')
    nrmval = 2;
end

% Set some colors
C = colormap('lines');

% Data about the tensor
r = ncomponents(M);

% Set height parameters
toppx = 25;
btmpx = 35;
factpx = 178;
hspx = 3;
hpx = r*factpx + (r-1)*hspx + toppx + btmpx;

% Set width parameters (absolute pixels)
ltpx = 40;
rtpx = 5;
wspx = 755;
wpx = wspx + ltpx + rtpx;

% Set up plot commands
pc1 = @(x,y) bar(x,y,0.8,'FaceColor',C(1,:),'EdgeColor',C(1,:)*0.5);
pc2 = @(x,y) plot(x,y,'.-','Color',C(5,:),'Linewidth',1);
pc3 = @(x,y) plot(x,y,'.-','Color',C(6,:),'Linewidth',1);

% Normalize M
M = fixsigns(normalize(M,'sort',2));
if nrmval == 0
    M = normalize(M,1);
end

% Run viz command
h = viz(M, 'Figure', figid, 'BaseFontSize', 12, 'Normalize', 0, ...
    'PlotCommands',{pc1, pc2, pc3},...
    'ModeTitles', {'Sample', 'Emission', 'Excitation'}, ...
    'LeftSpace', ltpx/wpx, 'RightSpace', rtpx/wpx, ...
    'TopSpace', toppx/hpx, 'BottomSpace', btmpx/hpx, ...
    'HorzSpace', hspx/hpx);

if ~isempty(M2) 
    if isa(M2,'ktensor') % Show a second Kruskal tensor in the same plot!       
        
        M2 = fixsigns(normalize(M2,'sort',2));       
        [~,M2] = score(M2,M,'lambda_penalty',true);
        if nrmval == 0
            M2 = normalize(M2,1);
        end
        
        % Mode 1
        A = M.U{1};
        B = M2.U{1}; 
        AB = [A B];
        yl = [min( -0.01, min(AB(:)) ), max( 0.01, max(AB(:)) )];
        for j = 1:r
            hold(h.FactorAxes(1,j),'off');
            axes(h.FactorAxes(1,j));
            bar([A(:,j) B(:,j)], 'grouped')
            ylim(h.FactorAxes(1,j),yl);
            set(h.FactorAxes(1,j),'Ytick',[]);
            set(h.FactorAxes(1,j),'FontSize',12)
            if j < 3
                set(h.FactorAxes(1,j),'XTickLabel',{});
            end
        end
        
        % Mode 2
        U2 = M2.U{2};
        for j = 1:r
            hold(h.FactorAxes(2,j),'on');  
            axes(h.FactorAxes(2,j));
            xx = (1:size(M2,2))';
            yy = U2(:,j);
            plot(xx,yy,'--','Color',C(2,:),'Linewidth',1);  
            hold(h.FactorAxes(2,j),'off'); 
        end
        
        % Mode 3
        U3 = M2.U{3};
        for j = 1:r
            hold(h.FactorAxes(3,j),'on');  
            axes(h.FactorAxes(3,j));
            xx = (1:size(M2,3))';
            yy = U3(:,j);
            plot(xx,yy,'--','Color',C(2,:),'Linewidth',1);  
            hold(h.FactorAxes(3,j),'off'); 
        end
        
        % Component labels
        rellambda1 = M.lambda/M.lambda(1);
        rellambda2 = M2.lambda/M2.lambda(1);
        for j = 1:r
            newtxt = sprintf('%3.2f\n vs.\n%3.2f', rellambda1(j), rellambda2(j));
            set(h.CompTitleHandles(j),'String',newtxt)
        end
        
    else % Add true mixtures
        if r ~= 3
            error('Can only include true mixtures for r=3 solutions')
        end
        A = M.U{1};
        B = M2;
        B = bsxfun(@rdivide,B,sqrt(sum(B.^2,1))); %<- Normalize
        [sc,tmp] = score(ktensor({B}),ktensor({A}),'lambda_penalty',false);
        Bp = tmp.U{1}; % reorder as needed
        AB = [A B];
        yl = [min( -0.01, min(AB(:)) ), max( 0.01, max(AB(:)) )];
        
        for j = 1:r
            hold(h.FactorAxes(1,j),'off');
            axes(h.FactorAxes(1,j));
            bar([A(:,j) Bp(:,j)], 'grouped')
            ylim(h.FactorAxes(1,j),yl);
            set(h.FactorAxes(1,j),'Ytick',[]);
            set(h.FactorAxes(1,j),'FontSize',12)
            if j == 1
                legend('Computed','True','FontSize',10);
            end
            if j < 3
                set(h.FactorAxes(1,j),'XTickLabel',{});
            end
        end
    end
end

for j = 1:r
    set(h.FactorAxes(2,j),'XLim',[0 250]);
    set(h.FactorAxes(2,j),'XTick',[25:50:250]);
end
foo = get(h.FactorAxes(2,r),'XTick');
set(h.FactorAxes(2,r),'XTickLabel',foo+250);

for j = 1:r
    set(h.FactorAxes(3,j),'XLim',[0 20]);
    set(h.FactorAxes(3,j),'XTick',[2:4:21]);
end
foo2 = get(h.FactorAxes(3,r),'XTick');
set(h.FactorAxes(3,r),'XTickLabel',5*foo2+210);




%%
width = wpx/100;     % Width in inches
height = hpx/100;    % Height in inches
pos = get(gcf, 'Position');
delta_y = max(0, height*100 - pos(4));
set(gcf, 'Position', [pos(1) (pos(2)-delta_y) width*100, height*100]); 

%%
if ~isempty(fname)
    exportgraphics(gcf,fname,'Resolution',300)
end