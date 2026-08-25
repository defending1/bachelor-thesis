%% Preprocessing for EEM data used in Tensor Decompositions textbook


%% Data Source Information
% The data was downloaded from http://www.models.life.ku.dk/joda/prototype.
% We use only the EEM data, stored in the `X` struct.
% 
% The data consists of EEM data from 28 samples containing different
% concentrations of five chemical compounds, of which we only consider
% those three detected by EEM: 
%
% * Valine-Tyrosine-Valine (Val-Tyr-Val) - peptide
% * Tryptophan-Glycine (Trp-Gly) - peptide
% * Phenylalanine (Phe) - amino acid
%
% The data acquisition was described as follows: "Fluorescence Spectroscopy
% data were acquired on a FS920 spectrophotometer (Edinburgh Instruments,
% Edinburgh, Scotland). Excitation Emission Matrix data were measured with
% excitation wavelengths from 210 nm to 310 nm with an increment of 5 nm
% for each scan, and emission wavelengths from 250 nm to 500 nm with an
% increment of 1 nm. In order to avoid 1st order Rayleigh scatter, emission
% data were not acquired in an interval of 10 nm from the excitation
% wavelength. Excitation and emission monochromator slit widths were set at
% 5 nm and integration time was 0.1 s/nm. Every sample day a blank sample
% was measured and subtracted from the samples to eliminate interference
% from the water Raman signal. Due to the very different quantum yields for
% the three aromatic amino acids we adjusted the concentrations for the
% fluorescence experiment. Val-Tyr-Val was diluted 70 times, Trp-Gly was
% diluted 1000 times, and Phe was doubled in concentration."

%% True Concentrations
% As reported in http://www.models.life.ku.dk/~acare/Table1.png.
% Columns correspond to Val-Tyr-Val, Trp-Gly, and Phe, respectively.
% Mixture 27 is *not* included in the dataset and so omitted here.
% There are some zero rows and repeat rows because we ignore the compounts
% that cannot be measured by EEM.

compound_names = {'Val-Tyr-Val', 'Trp-Gly', 'Phe'};

mixtures = [...
    5.0000         0         0
         0    5.0000         0
         0         0    5.0000
         0         0         0 %<- Removed below (4)
         0         0         0 %<- Removed below (5)
    1.2500    5.0000    3.7500
    3.7500    1.2500    5.0000
    2.5000    5.0000    2.5000 %<- Removed below (8)
    5.0000    3.7500    2.5000
    3.7500    3.7500    5.0000
    6.2500    1.2500    1.2500
    1.2500    5.0000    2.5000
    2.5000    6.2500    2.5000
    5.0000    1.2500    3.7500
    1.2500    3.7500    2.5000
    3.7500    3.7500    1.2500 %<- Removed below (15)
    2.5000    3.7500    1.2500
    1.2500         0    5.0000 %<- Removed below (17)
    3.7500         0    2.5000
    2.5000         0    3.7500 %<- Removed below (19)
    5.0000         0    1.2500
    3.7500         0    3.7500
    5.0000         0    1.2500
    1.2500         0    5.0000 %<- Removed below (23)
    2.5000         0    2.5000 %<- Removed below (24)
    5.0000         0    1.2500 %<- Removed below (25)
    3.7500         0    5.0000 %<- Removed below (26)
    2.5000         0    2.5000
    ];

%% Downselect to unique and non-zero mixtures of the compounds
[~,ii] = unique(mixtures,'row','stable');
omitmixtures = [ 0 0 0; 1.25 0 5; 2.5 0 2.5; 3.75 3.75 1.25; 2.5 5 2.5];
tf = ~ismember(mixtures(ii,:), omitmixtures,'row');
ii = ii(tf);
mixtures = mixtures(ii,:);

%% Load data
% The original datafile can be downloaded here:
% http://www.models.life.ku.dk/sites/default/files/EEM_NMR_LCMS.mat .
% The data we want is in X. Note that some entries are NaN, representing
% data points for which nothing was collected.
load('EEM_NMR_LCMS.mat');
Xraw = tensor(X.data(ii,:,:)); %<- Extract only some mixtures
clear X Y Z

%% Setup metadata
mode_titles = {'Sample','Emission','Excitation'};
mode_ranges = {(1:size(mixtures,1))', (250:1:500)', (210:5:310)'};

%% Filling in Missing Data using WOPT
% We fill in the missing data using the solution obtained by CP-WOPT, per
% the procedure below.

%% (1) Solve multiple times with WOPT
rng('default');
ntrials = 10;
results = cell(ntrials,1);
W = tensor(~isnan(Xraw.data));
for t = 1:ntrials
    [M,~,info] = cp_wopt(Xraw,W,3,'lower',0);
    results{t}.M = M;
    results{t}.feval = info.f;
end
%% (2) Select best solution
[fmin,tmin] = max(cellfun(@(x) x.feval, results));
M = results{tmin}.M;
feval = fmin;

%% (3) Fill in missing data *and* values less than zero in original tensor
Mdata = double(full(M));
Xdata = Xraw.data;
fillidx = isnan(Xdata) | (Xdata<0);
Xdata(fillidx) = Mdata(fillidx);
X = tensor(Xdata);

%% Report quality of solution
fit = 1 - norm(X-full(M))/norm(X)
s = score(ktensor({M.U{1}}),ktensor({mixtures}),'lambda_penalty',false)

%% Save into MATLAB files
fname = 'EEM18.mat';
save(fname, 'compound_names', 'mixtures');
save(fname,'-append','mode_titles','mode_ranges');
save(fname,'-append','Xraw','X');

