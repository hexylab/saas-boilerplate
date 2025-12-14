#!/usr/bin/env node
/**
 * CDK application entry point.
 */

import * as cdk from 'aws-cdk-lib';

import { CognitoStack } from '../lib/cognito-stack';
import { DatabaseStack } from '../lib/database-stack';
import { NetworkStack } from '../lib/network-stack';

const app = new cdk.App();

// Get environment from context or use defaults
const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION || 'ap-northeast-1',
};

const environment = app.node.tryGetContext('environment') || 'dev';
const projectName = '{{ project_slug }}';

// Create stacks
const networkStack = new NetworkStack(app, `${projectName}-network-${environment}`, {
  env,
  projectName,
  environment,
});

const databaseStack = new DatabaseStack(app, `${projectName}-database-${environment}`, {
  env,
  projectName,
  environment,
  vpc: networkStack.vpc,
});

const cognitoStack = new CognitoStack(app, `${projectName}-cognito-${environment}`, {
  env,
  projectName,
  environment,
});

// Add dependencies
databaseStack.addDependency(networkStack);
