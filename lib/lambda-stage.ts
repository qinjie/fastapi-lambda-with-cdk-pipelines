import * as cdk from "@aws-cdk/core";
import { CfnOutput } from "@aws-cdk/core";
import { LambdaStack } from "./lambda-stack";

export class LambdaStage extends cdk.Stage {
  outputLambda: CfnOutput;
  outputApiGateway: CfnOutput;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StageProps) {
    super(scope, id, props);

    const stackAlpha = new LambdaStack(this, `${id}LambdaStack`, {
      tags: {
        Application: `${id}`,
        Environment: id,
      },
    });
    this.outputLambda = stackAlpha.outputLambda;
    this.outputApiGateway = stackAlpha.outputApiGateway;
  }
}
