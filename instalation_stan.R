remove.packages("rstan")
if (file.exists(".RData")) file.remove(".RData")


install.packages("rstan", repos = "https://cloud.r-project.org/", dependencies = TRUE)


example(stan_model, package = "rstan", run.dontrun = TRUE)
quit()


# Compile packages using all cores
Sys.setenv(MAKEFLAGS = paste0("-j",parallel::detectCores()))

install.packages(c("StanHeaders","rstan"),type="source")


install.packages(c("StanHeaders","rstan"),type="source")


install.packages("StanHeaders", repos = c("https://mc-stan.org/r-packages/", getOption("repos")))
install.packages("rstan", repos = c("https://mc-stan.org/r-packages/", getOption("repos")))
