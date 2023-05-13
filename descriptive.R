library(rstan)

data  <- read.csv('teams_stats.csv', sep = ',', header = TRUE)
View(data)

boxplot(gpm ~ region, data = data, main = 'GPM by region', xlab = 'Region', ylab = 'GPM')
boxplot(dpm ~ region, data = data, main = 'DPM by region', xlab = 'Region', ylab = 'DPM')
boxplot(kpg ~ region, data = data, main = 'KPM by region', xlab = 'Region', ylab = 'KPM')
boxplot(dpg ~ region, data = data, main = 'DPG by region', xlab = 'Region', ylab = 'DPG')

# mean of gold per minute by region
euw_gpm <- mean(subset(data, region == 'EUW')$gpm)
kr_gpm <- mean(subset(data, region == 'KR')$gpm)
pcs_gpm <- mean(subset(data, region == 'PCS')$gpm)
na_gpm <- mean(subset(data, !(region %in% c('EUW', 'KR', 'PCS', 'CN', 'VN')))$gpm)
cn_gpm <- mean(subset(data, region == 'CN')$gpm)
vn_gpm <- mean(subset(data, region == 'VN')$gpm)
mean_gpm_vector <- c(euw_gpm, kr_gpm, pcs_gpm, na_gpm, cn_gpm, vn_gpm)
mean_gpm_vector

# mean of damage per minute by region
euw_dpm <- mean(subset(data, region == 'EUW')$dpm)
kr_dpm <- mean(subset(data, region == 'KR')$dpm)
pcs_dpm <- mean(subset(data, region == 'PCS')$dpm)
na_dpm <- mean(subset(data, !(region %in% c('EUW', 'KR', 'PCS', 'CN', 'VN')))$dpm)
cn_dpm <- mean(subset(data, region == 'CN')$dpm)
vn_dpm <- mean(subset(data, region == 'VN')$dpm)
mean_dpm_vector <- c(euw_dpm, kr_dpm, pcs_dpm, na_dpm, cn_dpm, vn_dpm)
mean_dpm_vector

# mean of kills per game by region
euw_kpg <- mean(subset(data, region == 'EUW')$kpg)
kr_kpg <- mean(subset(data, region == 'KR')$kpg)
pcs_kpg <- mean(subset(data, region == 'PCS')$kpg)
na_kpg <- mean(subset(data, !(region %in% c('EUW', 'KR', 'PCS', 'CN', 'VN')))$kpg)
cn_kpg <- mean(subset(data, region == 'CN')$kpg)
vn_kpg <- mean(subset(data, region == 'VN')$kpg)
mean_kpg_vector <- c(euw_kpg, kr_kpg, pcs_kpg, na_kpg, cn_kpg, vn_kpg)
mean_kpg_vector

# mean of deaths per game by region
euw_dpg <- mean(subset(data, region == 'EUW')$dpg)
kr_dpg <- mean(subset(data, region == 'KR')$dpg)
pcs_dpg <- mean(subset(data, region == 'PCS')$dpg)
na_dpg <- mean(subset(data, !(region %in% c('EUW', 'KR', 'PCS', 'CN', 'VN')))$dpg)
cn_dpg <- mean(subset(data, region == 'CN')$dpg)
vn_dpg <- mean(subset(data, region == 'VN')$dpg)
mean_dpg_vector <- c(euw_dpg, kr_dpg, pcs_dpg, na_dpg, cn_dpg, vn_dpg)
mean_dpg_vector

#all data







# unique(data$region)

# N <- nrow(data)

# fit <- stan(file='stan_models/linear_reg.stan', data = list(N = nrow(data), x = data$kpg, y = data$wins), iter = 1000, chains = 4)

# posterior <- extract(fit)
# View(posterior)

# mean(posterior$alpha)
# mean(posterior$beta)
