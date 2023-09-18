class BaseProtocolParams:
    protocolnames = tuple()

    def is_protocol(self, protocol_name) -> bool:
        return protocol_name.lower() in self.protocolnames.lower()


class PairedPulseFamilyParams:
    protocolnames = ("ledpairedpulsefamily", "ledpairedpuslefamilyoriginal",)

    def __init__(self, protocol, epoch):
        self.params = dict(
            intime=protocol["inTime"],
            intime2=epoch.group["protocolParameters"].attrs["inTime"],
            intimeadditive=protocol["inTimeAdditive"],
            led=protocol["led"],
            lightmean=protocol["lightMean"],
            pretime=protocol["preTime"],
            lightamplitude1=protocol["lightAmplitude1"],
            lightamplitude2=protocol["lightAmplitude2"],
            stimtime1=protocol["stimTime1"],
            stimtime2=protocol["stimTime2"],
            tailtime=protocol["tailTime"],
        )


class ChirpStimulusLedParams:
    protocolnames = ("chirpstimulusled",)

    def __init__(self, protocol):
        self.params = dict(
            contrastmax=protocol["contrastMax"],
            backgroundintensity=protocol["backgroundIntensity"],
            contrastfrequency=protocol["contrastFrequency"],
            contrastmin=protocol["contrastMin"],
            contrasttime=protocol["contrastTime"],
            frequencycontrast=protocol["frequencyContrast"],
            frequencymax=protocol["frequencyMax"],
            frequencymin=protocol["frequencyMin"],
            frequencytime=protocol["frequencyTime"],
            intertime=protocol["interTime"],
            stepcontrast=protocol["stepContrast"],
            steptime=protocol["stepTime"],
            led=protocol["led"],
        )


class ExpandingSpotsParams:
    protocolnames = ("expandingspots",)

    def __init__(self, protocol, epoch):
        self.params = dict(
            current_spot_size=epoch.protocol_parameters("currentSpotSize"),
            randomize_order=protocol["randomizeOrder"],
            sample_rate=protocol["sampleRate"],
            spot_intensity=protocol["spotIntensity"],
            spot_sizes=protocol["spotSizes"],
            background_intensity=protocol["backgroundIntensity"],
        )


class AdapatingSteps:
    protocolnames = ("adapatingsteps",)

    def __init__(self, protocol, epoch):
        self.params = dict(
            baseline_magnitude=protocol["baselineMagnitude"],
            step_magnitude=protocol["stepMagnitude"],
            flash_duration=protocol["flashDuration"],
            fixed_post_flash_amp=protocol["fixedPostFlashAmp"],
            fixed_pre_flash_amp=protocol["fixedPreFlashAmp"],
            fixed_step_flash_amp=protocol["fixedStepFlashAmp"],
            fixed_post_flash_time=protocol["fixedPostFlashTime"],
            fixed_pre_flash_time=protocol["fixedPreFlashTime"],
            fixed_step_flash_time=protocol["fixedStepFlashTime"],
            step_stim=protocol["stepStim"],
            step_pre=protocol["stepPre"],
            step_tail=protocol["stepTail"],
            variable_flash_times=protocol["variableFlashTimes"],
            variable_flash_time=epoch.protocol_parameters("variableFlashTime"),
            variable_post_flash_amp=protocol["variablePostFlashAmp"],
            variable_step_flash_amp=protocol["variableStepFlashAmp"],
        )
