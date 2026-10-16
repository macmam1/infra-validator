// Stormkit serverless function
// Returns all environment variables to help debug runtime config
export default (req, res) => {
  const env = {};
  for (const [key, value] of Object.entries(process.env)) {
    // Mask sensitive values
    if (key.match(/KEY|SECRET|PASS|TOKEN|API/i)) {
      env[key] = '***';
    } else {
      env[key] = value;
    }
  }
  res.status(200).json({
    status: 'ok',
    service: 'infra-validator',
    timestamp: new Date().toISOString(),
    env: env,
    nodeVersion: process.version,
  });
};
