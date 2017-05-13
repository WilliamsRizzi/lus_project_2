.PHONY: clean compare

all: computations/model_1 computations/model_2 compare

data:
	@./scripts/preprocess.sh

computations/model_1: data
	@./scripts/run.sh 1

computations/model_2: data
	@./scripts/run.sh 2

compare: 
	@./scripts/compare.sh

clean:
	@rm -rf data
	@rm -rf computations
