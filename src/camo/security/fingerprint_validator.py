class FingerprintConsistencyValidator:
    @staticmethod
    def validate(fingerprint: dict) -> dict:
        """
        Validates internal consistency preventing impossible hardware combinations natively protecting against advanced bot checks safely.
        """
        os_type = fingerprint.get("platform", "").lower()
        ua = fingerprint.get("userAgent", "").lower()
        gpu = fingerprint.get("gpuVendor", "").lower()

        if "win" in os_type and "mac" in ua:
            return {"status": "invalid", "reason": "User-Agent implies Mac but Platform is Windows"}

        if "mac" in os_type and ("win" in ua or "linux" in ua):
            return {"status": "invalid", "reason": "User-Agent implies Windows/Linux but Platform is Mac"}

        if "mac" in os_type and "intel" not in gpu and "apple" not in gpu:
            return {"status": "invalid", "reason": "GPU incompatible with OS (Mac implies Intel/Apple GPU)"}

        # Add basic timezone validation mock
        # Real application would verify against an active ip-lookup table

        return {"status": "valid"}

fingerprint_validator = FingerprintConsistencyValidator()
