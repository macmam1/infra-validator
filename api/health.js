// Stormkit serverless function
export default (req, res) => {
  res.status(200).json({
    status: 'ok',
    service: 'infra-validator',
    timestamp: new Date().toISOString(),
    nodeVersion: process.version,
    PORT: process.env.PORT || 'not set',
  });
};
