from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(events=["build_message"], mappings={"message": "m", "punctuation": "p"})
class TemplateFlow(FlowSpec):

    message = Parameter(name="message", required=True, type=str)
    punctuation = Parameter(name="punctuation", required=True, type=str)

    @step
    def start(self):
        if self.message != "Hola":
            raise RuntimeError("Unexpected message: %s" % self.message)
        if self.punctuation != "!":
            raise RuntimeError("Unexpected punctuation: %s" % self.punctuation)
        self.next(self.end)

    @step
    def end(self):
        print("Message: %s%s" % (self.message, self.punctuation))


if __name__ == "__main__":
    TemplateFlow()
