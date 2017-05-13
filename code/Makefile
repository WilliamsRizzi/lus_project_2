.PHONY: clean

all: model_1 model_2

data:
	@./scripts/preprocess.sh

model_1: data
	@./scripts/run.sh 1

model_2: data
	@./scripts/run.sh 2

clean:
	@rm -rf data
	@rm -rf computations
