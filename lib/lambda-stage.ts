import * as cdk from "@aws-cdk/core";
import { CfnOutput } from "@aws-cdk/core";
import { LambdaAlphaStack } from "./lambda-stack";
import { IFunction } from "@aws-cdk/aws-lambda";

export class LambdaStage extends cdk.Stage {
  output: CfnOutput;
  func: IFunction;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StageProps) {
    super(scope, id, props);

    const stackAlpha = new LambdaAlphaStack(this, "LambdaAlpha", {
      tags: {
        Application: "LambdaAlpha",
        Environment: id,
      },
    });
    this.func = stackAlpha.lambdaFunction;
    this.output = stackAlpha.outputLambda;
  }
}
